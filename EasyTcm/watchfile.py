import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pymysql
from _baselib import split_path_os


def update_record_status_and_url(saved_filename, new_status, new_url):
    # 数据库连接信息
    db_config = {
        'host': '127.0.0.1',  # 如果数据库在本地服务器上
        'port': 3306,  # MySQL默认端口
        'user': 'root',
        'password': 'root1234',
        'database': 'web8',
        'charset': 'utf8mb4'  # 支持更多的字符集，比如emoji
    }

    # SQL 更新语句
    update_sql = """
    UPDATE dataminer_upload_records
    SET status = %s, url = %s
    WHERE saved_filename = %s
    """

    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # 执行SQL语句
            affected_rows = cursor.execute(update_sql, (new_status, new_url, saved_filename))

            # 提交更改
            connection.commit()

        # 关闭连接
        connection.close()

        if affected_rows > 0:
            print(f"成功更新 {affected_rows} 行记录")
        else:
            print("没有找到匹配的记录进行更新")

    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
        # 在发生错误时可以尝试回滚
        if 'connection' in locals():
            connection.rollback()
        raise


# 使用示例
# update_record_status_and_url('example_saved_filename.txt', 'processed', 'http://example.com/path/to/file')
from main import dm1


class ChangeHandler(FileSystemEventHandler):
    """定义处理文件变化的类"""

    def on_created(self, event):
        if not event.is_directory:
            print(f"Created file: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified file: {event.src_path}")
            folder, filename = split_path_os(event.src_path)
            time.sleep(5)  # 延迟一秒，等待文件写入完成
            print(f"文件 {filename} 已写入，开始更新数据库记录")
            import os
            if not os.path.exists(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}'):
                os.makedirs(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}')
                # 移动文件到指定文件夹
                os.rename(event.src_path, f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}\\{filename}')
                update_record_status_and_url(filename, '已接收', '...')
                result = dm1(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}\\{filename}')
                if result is not None:
                    print(f"文件 {filename} 已处理完成，开始更新数据库记录")
                    update_record_status_and_url(filename, '处理成功', f'http://localhost/dms/{result}.zip')
                else:
                    print(f"文件 {filename} 处理失败，请检查日志")
                    update_record_status_and_url(filename, '处理失败，请按模板上传', '...')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Deleted file: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"Moved file from {event.src_path} to {event.dest_path}")


def start_monitoring(path_to_watch='D:\\dataminer'):
    """启动对指定路径的监控"""
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    print(f"Starting monitoring on {path_to_watch}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitoring.")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    # 调用函数开始监控
    start_monitoring()
