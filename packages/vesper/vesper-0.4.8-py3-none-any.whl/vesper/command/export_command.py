"""Module containing class `ExportCommand`."""


import logging

from vesper.command.command import Command, CommandSyntaxError
from vesper.singletons import extension_manager
import vesper.command.command_utils as command_utils
import vesper.django.app.model_utils as model_utils
import vesper.util.text_utils as text_utils


_logger = logging.getLogger()


class ExportCommand(Command):
    
    
    extension_name = 'export'
    
    
    def __init__(self, args):
        
        super().__init__(args)
        
        get = command_utils.get_required_arg
        self._exporter_spec = get('exporter', args)
        self._detector_names = get('detectors', args)
        self._sm_pair_ui_names = get('station_mics', args)
        self._classification = get('classification', args)
        self._start_date = get('start_date', args)
        self._end_date = get('end_date', args)
        
        self._exporter = self._create_exporter()
        
        
    def _create_exporter(self):
        
        try:
            name, arguments = _parse_exporter_spec(self._exporter_spec)
            return _create_exporter(name, arguments)
        
        except Exception as e:
            command_utils.log_and_reraise_fatal_exception(
                e, 'Exporter construction')
            
        
    def execute(self, job_info):
        
        self._exporter.begin_exports()
    
        annotation_name, annotation_value = \
            model_utils.get_clip_query_annotation_data(
                'Classification', self._classification)
            
        value_tuples = self._create_clip_query_values_iterator()
        
        for detector, station, mic_output, date in value_tuples:
            
            clips = _get_clips(
                station, mic_output, detector, date, annotation_name,
                annotation_value)
            
            count = clips.count()
            count_text = text_utils.create_count_text(count, 'clip')
            
            _logger.info((
                'Exporter will visit {} for detector "{}", station "{}", '
                'mic output "{}", and date {}.').format(
                    count_text, detector.name, station.name, mic_output.name,
                    date))
            
            try:
                _export_clips(clips, self._exporter)
                    
            except Exception:
                _logger.error(
                    'Clip export failed. See below for exception traceback.')
                raise
            
        self._exporter.end_exports()
            
        return True


    def _create_clip_query_values_iterator(self):
        
        try:
            return model_utils.create_clip_query_values_iterator(
                self._detector_names, self._sm_pair_ui_names,
                self._start_date, self._end_date)
            
        except Exception as e:
            command_utils.log_and_reraise_fatal_exception(
                e, 'Clip query values iterator construction')
            
            
def _parse_exporter_spec(spec):
    
    try:
        name = spec['name']
    except KeyError:
        raise CommandSyntaxError('Missing required exporter name.')
    
    arguments = spec.get('arguments', {})
    
    return name, arguments


def _create_exporter(name, arguments):
    
    classes = extension_manager.instance.get_extensions('Exporter')
    
    try:
        cls = classes[name]
    except KeyError:
        raise ValueError('Unrecognized exporter "{}".'.format(name))
    
    return cls(arguments)


def _get_clips(*args):
    try:
        return model_utils.get_clips(*args)
    except Exception as e:
        command_utils.log_and_reraise_fatal_exception(e, 'Clip query')
    
    
def _create_clip_count_text(count):
    suffix = '' if count == 1 else 's'
    return '{} clip{}'.format(count, suffix)
        

_LOGGING_PERIOD = 500    # clips


def _export_clips(clips, exporter):
    
    visited_count = 0
    exported_count = 0
    
    for clip in clips:
        
        if exporter.export(clip):
            exported_count += 1
        
        visited_count += 1
        
        if visited_count % _LOGGING_PERIOD == 0:
            _logger.info('Visited {} clips...'.format(visited_count))
            
    _logger.info(
        'Exported {} of {} visited clips.'.format(
            exported_count, visited_count))
