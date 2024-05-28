from typing import Dict

import threading
from threading import Thread

import time

from events import *


class Microservice:
    '''
    Абстрактный класс микросервиса
    Все микросервисы должны его наследовать
    Для него должна быть реализована функция `self.handle_event(event: Event)`
    '''

    DEFAULT_QUEUE_CHECK_TIMER = 10.0
    MINIMAL_QUEUE_CHECK_TIMER = 0.5

    def __init__(self, event_queue: Queue, writers: Dict[str, KafkaEventWriter]):
        '''
        Инициализация класса:
        - `event_queue` - очередь приходящих событий
        - `writers` - словарь, где ключ - название микросервиса, значение - писатель событий в этот микросервис
        Поля класса:
        - `self.event_queue` - очередь приходящих событий
        - `self.writers` - словарь, где ключ - название микросервиса, значение - писатель событий в этот микросервис
        - `self.queue_check_timer` - кол-во секунд ожидаемое перед каждой проверкой очереди событий
        - `self.running` - мультипоточное булевое значение, указывающее состояние микросервиса
        - `self.runnning_thread` - указатель на поток, в котором запущен микросервис 
        '''

        self.event_queue = event_queue
        self.writers = writers

        self.queue_check_timer = self.DEFAULT_QUEUE_CHECK_TIMER

        self.running = threading.Event()
        self.running.set()

        self.running_thread = Thread(target=self.run)
        self.running_thread.start()

    def set_queue_check_timer(self, seconds: float):
        self.queue_check_timer = max(seconds, self.MINIMAL_QUEUE_CHECK_TIMER)

    def run(self):
        '''
        Принятие событий из очереди 
        '''

        while self.running.is_set():

            if self.event_queue.empty():
                time.sleep(self.queue_check_timer)
                continue

            self.handle_event(self.event_queue.get())

    '''
    Пример реализуемого функционала микросервиса:
    def handle_event(self, event: Event):
        match event.type:
            case EventType.TrendData:
                self.handle_event_trend_data(event.data)
            case EventType.TrendAnalyseResult:
                self.handle_event_trend_analyse_result(event.data)
            case _:
                pass

    def handle_event_trend_data(self, trend_data: TrendData):
        self.dm_ai_event_writer.send_event(Event(EventType.TrendData, trend_data))

    def handle_event_trend_analyse_result(self, scale_data: ScaleData):
        deployment = self.k8s_api.read_namespaced_deployment(self.target_deployment, self.target_namespace)
        deployment.spec.replicas = scale_data.replica_count
        _api_response = self.k8s_api.patch_namespaced_deployment(
            name=self.target_deployment,
            namespace=self.target_namespace,
            body=deployment
        )
    '''

    def stop(self):
        self.running.clear()
        self.running_thread.join()
