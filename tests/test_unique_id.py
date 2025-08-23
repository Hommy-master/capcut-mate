import unittest
import time
import threading
from src.utils.unique_id import UniqueIDGenerator


class TestUniqueIDGenerator(unittest.TestCase):
    def test_singleton_pattern(self):
        # 测试单例模式是否生效
        generator1 = UniqueIDGenerator()
        generator2 = UniqueIDGenerator()
        self.assertIs(generator1, generator2, "单例模式验证失败：返回了不同的实例")

    def test_id_format(self):
        # 测试ID格式是否正确
        generator = UniqueIDGenerator()
        id1 = generator.generate()
        print("\nid1: " + id1)
        self.assertEqual(len(id1), 20, f"ID长度不正确: {len(id1)}，应为20")
        self.assertTrue(id1.isdigit(), f"ID应只包含数字: {id1}")

        # 等待1秒，确保下一个ID使用新的时间戳
        time.sleep(1)
        id2 = generator.generate()
        print("\nid2: " + id2)
        self.assertEqual(len(id2), 20, f"ID长度不正确: {len(id2)}，应为20")
        self.assertTrue(id2.isdigit(), f"ID应只包含数字: {id2}")

    def test_duplicate_in_same_timestamp(self):
        # 测试同一时间戳内生成的ID是否不同
        generator = UniqueIDGenerator()
        ids = set()
        # 生成多个ID，理论上在同一秒内应该生成不同的ID
        for _ in range(10):
            ids.add(generator.generate())
        self.assertEqual(len(ids), 10, "同一时间戳内生成了重复的ID")

    def test_different_timestamps(self):
        # 测试不同时间戳生成的ID是否不同
        generator = UniqueIDGenerator()
        id1 = generator.generate()
        # 等待1秒，确保下一个ID使用新的时间戳
        time.sleep(1)
        id2 = generator.generate()
        self.assertNotEqual(id1, id2, "不同时间戳生成了相同的ID")
        # 验证前14位是否为时间戳（年月日时分秒）
        self.assertNotEqual(id1[:14], id2[:14], "不同时间戳的ID前14位应该不同")

    def test_thread_safety(self):
        # 测试多线程环境下的线程安全性
        generator = UniqueIDGenerator()
        ids = set()
        ids_lock = threading.Lock()

        def generate_ids(count):
            local_ids = []
            for _ in range(count):
                local_ids.append(generator.generate())
            with ids_lock:
                ids.update(local_ids)

        # 创建多个线程同时生成ID
        threads = []
        thread_count = 5
        ids_per_thread = 100
        for _ in range(thread_count):
            thread = threading.Thread(target=generate_ids, args=(ids_per_thread,))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 验证生成的ID总数是否正确且无重复
        expected_count = thread_count * ids_per_thread
        self.assertEqual(len(ids), expected_count, f"多线程环境下生成了重复的ID，期望{expected_count}个唯一ID，实际{len(ids)}个")


if __name__ == '__main__':
    unittest.main()