#-*- coding:utf-8 -*-
import os
import datetime
import traceback
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from django.core.management import call_command

from apps.main_functions.fortasks import search_process
from apps.main_functions.files import open_file, check_path
from apps.main_functions.models import Tasks

logger = logging.getLogger('main')

def run_task(task):
    """Запускает фоновую задачу из Tasks очереди
       :param task: фоновая задача, где task.command - команда строкой
    """
    opts = {}
    command = task.command
    # Саму себя не выполняем
    if not command or 'tasks' in command:
        task.delete()
        return

    now = datetime.datetime.today().strftime('%H:%M:%S %d/%m/%Y')
    logger.info("START: %s" % now)

    with open_file('tasks_errors.txt', 'a+') as ferrors:

        ferrors.write('%s - %s\n' % (now, command))

        if '--' in command:
            cur_name = command.split('--')
            command = cur_name[0].strip()
            for i in range(len(cur_name)):
                if i == 0:
                    continue
                if cur_name[i]:
                    if '=' in cur_name[i]:
                        key, value = cur_name[i].split('=', 1)
                        key = str(key.strip())
                        value = value.strip()
                        opts[key] = value
                    else:
                        key = cur_name[i].strip()
                        opts[key] = True
        try:
            task.delete()
            call_command(command, **opts)
        except:
            error = traceback.format_exc()
            ferrors.write('%s\n' % error)


class Command(BaseCommand):
    """Выполняем задачи, поставленные в очередь
       !TODO ротация лога выполненных задач
    """
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--log',
            action = 'store_true',
            dest = 'log',
            default = False,
            help = 'Show logs')
        parser.add_argument('--index',
            action = 'store_true',
            dest = 'index',
            default = False,
            help = 'Partial djapian index')
        parser.add_argument('--rebuild_index',
            action = 'store_true',
            dest = 'rebuild_index',
            default = False,
            help = 'Full rebuild djapian index')
        parser.add_argument('--model',
            action = 'store',
            dest = 'model',
            type = str,
            default = False,
            help = 'Set model for work with index')
        parser.add_argument('--indexer',
            action = 'store',
            dest = 'indexer',
            type = str,
            default = False,
            help = 'Set specific indexer for index')

    def handle(self, *args, **options):
        """Работа с задачами Tasks"""
        # Вывод логов
        if options.get('log'):
            if check_path('tasks_errors.txt'):
                logger.info('empty file')
                return
            with open_file('tasks_errors.txt', 'r') as f:
                content = f.read()
            print(content)
            return

        is_running = search_process(q = ('tasks', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        now = datetime.datetime.today()
        tasks = Tasks.objects.filter(is_active=True).order_by('updated')
        for task in tasks:
            if task.updated <= now:
                run_task(task)

    """ !TODO
    if "djapian" in settings.INSTALLED_APPS:
      from django.db.models.loading import get_model
      import djapian
      from djapian.models import Change
      from djapian.space import IndexSpace
      from djapian.database import Database
      djapian.load_indexes()

      # -------------------------------------
      # Если хотим задать какой-то конкретный
      # индекс или модель для переиндексации
      # -------------------------------------
      index_indexer = None
      index_model = None
      # -------------------------------------------
      # Если нужно поработать с конкретным индексом
      # -------------------------------------------
      if options.get("indexer"):
        ind = options['indexer']
        for item in IndexSpace.instances:
          for model, indexers in item.get_indexers().iteritems():
            for indexer in indexers:
              cur_indexer = str(indexer).split(".")[-1]
              print "[INDEXER]:", cur_indexer
              if ind == cur_indexer:
                print "[USING]:", cur_indexer
                index_indexer = indexer
        if not index_indexer:
          print "[ERROR]: indexer not found"
          exit()

      # ------------------------------------------
      # Если нужно поработать с конкретной моделью
      # ------------------------------------------
      if options.get("model"):
        im = options['model']
        if not "." in im:
          print "[ERROR]: there is not dot"
          exit()
        im_array = im.split(".")
        if not len(im_array) == 2:
          print "[ERROR]: more than 2 parts"
          exit()
        app_label = im_array[0]
        model_name = im_array[1]
        index_model =  get_model(app_label, model_name)
        if not index_model:
          print "[ERROR]: model not found"
          exit()
        print "[WARN]: work with", index_model
        #for item in IndexSpace.instances:
          #for model, indexers in item.get_indexers().iteritems():
            #if model == index_model:

      # ---------------------
      # Полный ребилд индекса
      # ---------------------
      if options.get("rebuild_index"):
        import shutil
        Change.objects.all().delete()
        # ----------------------------------------------
        # Создаем альтернативную базу по всем индексам,
        # индексируем ее,
        # затем помещаем на место основной базы индексов
        # ----------------------------------------------
        djapian_folder = settings.DJAPIAN_DATABASE_PATH
        tmp_djapian_folder = os.path.join(djapian_folder, "TMP_DJAPIAN")
        for item in IndexSpace.instances:
          for model, indexers in item.get_indexers().iteritems():
            # -----------------------------
            # Работаем с конкретной моделью
            # -----------------------------
            if index_model:
              if not model == index_model:
                continue
            for indexer in indexers:
              # ------------------------------
              # Работаем с конкретным индексом
              # ------------------------------
              if index_indexer:
                if not indexer == index_indexer:
                  continue
                index_indexer = 1

              indexer_started = time.time()
              old_db_path = indexer._db._path
              new_db_path = old_db_path.replace(djapian_folder, tmp_djapian_folder)
              new_db = Database(new_db_path)
              indexer._db = new_db
              indexer.clear()
              indexer.update(None, None, 10000, False)
              indexer_elapsed = time.time() - indexer_started
              print indexer, "elapsed %.2f sec (%.2f min)" % (indexer_elapsed, indexer_elapsed/60)

              tmp = old_db_path + "_old"
              try:
                shutil.rmtree(tmp)
              except:
                pass
              try:
                shutil.move(old_db_path, tmp)
              except:
                pass
              try:
                shutil.move(new_db_path, old_db_path)
                print "[ALERT]: folder replaced", old_db_path
              except:
                print "[ERROR] folder not replaced"
              try:
                shutil.rmtree(tmp)
              except:
                pass

      # ----------
      # Индексация
      # ----------
      if options.get("index"):
        query = Change.objects.all()
        total_records = query.aggregate(Count("id"))['id__count']
        print total_records, "total_records"
        records_delete = query.filter(action="delete")
        total_records_delete = records_delete.aggregate(Count("id"))['id__count']
        print total_records_delete, "total_records_delete"

        # -----------------------------
        # Удаляем записи на удаление
        # их будем делать rebuild_index
        # -----------------------------
        records_delete.delete()

        ferrors.write(now.strftime("%d-%m-%Y %H:%M:%S")+" INDEXING...\n")
        index_opts = {"verbose":True, "verbosity":2, "traceback":True}
        call_command("index", **index_opts)

    ferrors.close()
    elapsed = time.time() - started
    print "epapsed %.2f sec (%.2f min)" % (elapsed, elapsed/60)
    """
