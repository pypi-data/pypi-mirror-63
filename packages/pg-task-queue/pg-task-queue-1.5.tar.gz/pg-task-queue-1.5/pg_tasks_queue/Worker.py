import sys
import json
import traceback
import importlib.util
import time
import threading
import datetime
import multiprocessing
from pg_tasks_queue.Database import TasksDatabase as database


class Worker(object):

    _timeout_sec = 60.
    _blocking = False
    _started = False
    _sleep_sec = 1.

    def init(self, config_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            if not isinstance(config_dict, dict):
                print(f'Error in {func_name}: not isinstance(database_dict, dict)...')
                return False
            database_dict = config_dict.get('database')
            if not isinstance(database_dict, dict):
                print(f'Error in {func_name}: not isinstance(database_dict, dict)...')
                return False
            if not database.init(database_dict):
                print(f'Error in {func_name}: not database.init(); return...')
                return False
            if not database.test_tables(create=False):
                print(f'Error in {func_name}: not database.test_tables(); return...')
                return False
            worker_cfg = config_dict.get('worker')
            if isinstance(worker_cfg, dict):
                self._timeout_sec = float(worker_cfg.get('timeout_sec', self._timeout_sec))
                self._sleep_sec = float(worker_cfg.get('sleep_sec', self._sleep_sec))
            return True
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return False

    def check_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            print(f'Error in {func_name}: module: "{module_name}" not found')
            return None
        else:
            return module_spec

    def import_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            module_spec = self.check_module(module_name)
            if module_spec is None:
                return None
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None

    def import_function_from_module(self, module_name, function_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            module = self.import_module(module_name)
            if module is None:
                return None
            if not hasattr(module, function_name):
                print(f'Error in {func_name}: module: "{module_name}"; function: "{function_name}" not found')
                return None
            return getattr(module, function_name)
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None

    def worker_process(self, queue, task_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}; task_dict: {task_dict}')
        task_module = task_dict.get('module')
        task_func = task_dict.get('func')
        func = self.import_function_from_module(task_module, task_func)
        if func is None:
            error = f'Error in {func_name}: import_function_from_module({task_module}, {task_func}) is None'
            print(error)
            result = {'error': error}
        else:
            params = task_dict.get('params')
            if isinstance(params, str):
                try:
                    params = json.loads(params)
                    if not isinstance(params, dict):
                        params = dict()
                    print(f'{func_name}: try to start "{task_module}.{task_func}"...')
                    result = func(**params)
                except Exception as e:
                    error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
                    print(error)
                    result = {'status': 'error', 'result': error}
        queue.put(result)

    def _do_task(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        if not self._started:
            print(f'{func_name}; self._started = False; return')
            return

        try:
            task_dict = database.get_one_task()
            print(f'{func_name}: now={datetime.datetime.now()}; task_dict: {task_dict}')
            if isinstance(task_dict, dict):
                queue = multiprocessing.Queue()
                worker = multiprocessing.Process(target=self.worker_process, args=(queue, task_dict,))
                worker.start()
                worker.join(timeout=self._timeout_sec)
                if worker.is_alive():
                    worker.terminate()
                    database.update_task_error(task_dict, f'Error in {func_name}: worker.terminate()')
                else:
                    if not queue.empty():
                        queue_get = queue.get_nowait()
                        if not isinstance(queue_get, dict):
                            error = f'Error in {func_name}: not isinstance(queue_get, dict)...'
                            print(error)
                            database.update_task_error(task_dict, error)
                        else:
                            status = queue_get.get('status')
                            result = queue_get.get('result', '')
                            if not isinstance(status, str):
                                error = f'Error in {func_name}: not isinstance(queue_get, dict)...'
                                print(error)
                                database.update_task_error(task_dict, error)
                            elif status == 'error':
                                database.update_task_error(task_dict, result)
                            else:
                                update_values = {'finished_time': datetime.datetime.now(),
                                                 'status': status,
                                                 'result': result}
                                database.update_task(task_dict.get('task_id'), update_values)
                    else:
                        error = f'Error in {func_name}: queue is empty()...'
                        print(error)
                        database.update_task_error(task_dict, error)

            if not self._blocking:
                threading.Timer(self._sleep_sec, self._do_task).start()

        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')

    def start(self, blocking=True, sleep_sec=None):
        self._blocking = blocking
        if isinstance(sleep_sec, float):
            self._sleep_sec = sleep_sec
        self._started = True
        if self._blocking:
            while self._started:
                self._do_task()
                time.sleep(self._sleep_sec)
        else:
            self._do_task()

    def stop(self):
        self._started = False
