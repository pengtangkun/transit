#!/usr/bin/env python3
# encoding: utf-8
# Author: burce.wang
# Description: 该脚本用于elasticsearch(6.3)指标深度采集
import json
import subprocess
import sys


class ElasticsearchCollect(object):

    def __init__(self):
        """
        初始化elasticsearch连接参数
        :param ip elasticsearch主机地址
        :param port elasticsearch连接端口
        """
        self.ip = ''
        self.port = ''
        self.username = ''
        self.passwd = ''

    def usage(self):
        print(
            """
            参数说明:
            --ip      : elasticsearch的ip
            --port    : elasticsearch的端口
            --username: elasticsearch的用户名
            --passwd  : elasticsearch的密码
            示例:
            python elasticsearch.py --ip 127.0.0.1 --port 18115 --username elastic --passwd 123456
            """.format(sys.argv[0]))

    def print_usage(self):
        if (len(sys.argv) < 2):
            self.usage()
            exit(1)
        elif sys.argv[1] != "--ip":
            print("no such option: {}".format(sys.argv[1]))
            exit(1)
        elif (len(sys.argv) == 2):
            self.usage()
            exit(1)
        elif (len(sys.argv) < 4):
            self.usage()
            exit(1)
        elif sys.argv[3] != "--port":
            print("no such option: {}".format(sys.argv[3]))
            exit(1)
        elif (len(sys.argv) == 4):
            self.usage()
            exit(1)
        self.ip = sys.argv[2]
        self.port = sys.argv[4]
        if (len(sys.argv)) == 5:
            return
        elif sys.argv[5] != "--username":
            print("no such option: {}".format(sys.argv[5]))
            exit(1)
        elif (len(sys.argv) == 6):
            self.usage()
            exit(1)
        elif (len(sys.argv) == 7):
            self.usage()
            exit(1)
        elif sys.argv[7] != "--passwd":
            print("no such option: {}".format(sys.argv[7]))
            exit(1)
        elif (len(sys.argv) == 8):
            self.usage()
            exit(1)
        elif (len(sys.argv) > 9):
            self.usage()
            sys.exit(1)
        self.username = sys.argv[6]
        self.passwd = sys.argv[8]

    @staticmethod
    def _run_cmd(cmd):
        """
        调用shell
        :param cmd:
        :return:
        """
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_stdout = bytes.decode(p.stdout)
        if cmd_stdout.endswith('\n'):
            cmd_stdout = cmd_stdout.strip()

        if p.returncode == '0':
            return None
        else:
            return cmd_stdout

    def get_nodes_name(self):
        """
        取nodes的名称（不同环境名称是不同的）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes']
        nodes_name_list = []
        for key in search_msg:
            nodes_name_list.append(key)
        nodes_name = nodes_name_list[0]
        return nodes_name

    def get_elasticsearch_breakers_accounting_limit_size_bytes(self, node_name):
        """
        accounting断路器最大内存限制
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['breakers']['accounting']['limit_size_in_bytes']
        return search_msg

    def get_elasticsearch_breakers_fielddata_limit_size_bytes(self, node_name):
        """
        列数据断路器最大内存限制
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['breakers']['fielddata']['limit_size_in_bytes']
        return search_msg

    def get_elasticsearch_breakers_in_flight_requests_limit_size_bytes(self, node_name):
        """
        请求中的断路器最大内存限制
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['breakers']['in_flight_requests']['limit_size_in_bytes']
        return search_msg

    def get_elasticsearch_breakers_parent_limit_size_bytes(self, node_name):
        """
        父断路器最大内存限制
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['breakers']['parent']['limit_size_in_bytes']
        return search_msg

    def get_elasticsearch_breakers_request_limit_size_bytes(self, node_name):
        """
        请求断路器最大内存限制
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['breakers']['request']['limit_size_in_bytes']
        return search_msg

    def get_elasticsearch_cluster_health_status(self):
        """
        集群健康状态
        :return:
        """
        cmd = "curl http://{}:{}/_cluster/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['status']
        return search_msg

    # todo
    def get_elasticsearch_cluster_health_up(self):
        pass

    def get_elasticsearch_clusterinfo_version_info(self):
        """
        elasticsearch版本信息
        :return:
        """
        cmd = "curl http://{}:{} -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        return search_msg

    def get_elasticsearch_filesystem_data_available_bytes(self, node_name):
        """
        块设备可用空间（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['fs']['data'][0]['available_in_bytes']
        return search_msg

    def get_elasticsearch_filesystem_data_free_bytes(self, node_name):
        """
        块设备空闲空间（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['fs']['data'][0]['free_in_bytes']
        return search_msg

    def get_elasticsearch_filesystem_data_size_bytes(self, node_name):
        """
        块设备总空间（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['nodes'][node_name]['fs']['data'][0]['total_in_bytes']
        return search_msg

    def get_elasticsearch_indices_docs(self):
        """
        节点上的文档数
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['docs']['count']
        return search_msg

    def get_elasticsearch_indices_docs_deleted(self):
        """
        节点上删除的文档数
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['docs']['deleted']
        return search_msg

    def get_elasticsearch_indices_flush_time_seconds(self):
        """
        累计刷新时间（秒）
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['flush']['total_time_in_millis']
        return search_msg

    def get_elasticsearch_indices_flush_total(self):
        """
        总刷新次数
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['flush']['total']
        return search_msg

    def get_elasticsearch_indices_query_miss_count(self):
        """
        查询miss数
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['query_cache']['miss_count']
        return search_msg

    def get_elasticsearch_indices_search_query_time_seconds(self):
        """
        查询总耗时
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["_all"]['total']['search']['query_time_in_millis']
        return search_msg

    def get_elasticsearch_indices_search_query_total(self):
        """
        查询总次数
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['search']['query_total']
        return search_msg

    def get_elasticsearch_indices_store_size_bytes(self):
        """
        已存储的索引数据大小（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg['_all']['total']['store']['size_in_bytes']
        return search_msg

    def get_elasticsearch_jvm_buffer_pool_used_bytes(self, node_name):
        """
        JVM缓存池当前用量（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['buffer_pools']['direct']['used_in_bytes']
        return search_msg

    def get_elasticsearch_jvm_gc_old_collection_seconds_count(self, node_name):
        """
        JVM老年代GC次数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['gc']['collectors']['old']['collection_count']
        return search_msg

    def get_elasticsearch_jvm_gc_young_collection_seconds_count(self, node_name):
        """
        JVM年轻代GC次数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['gc']['collectors']['young']['collection_count']
        return search_msg

    def get_elasticsearch_jvm_gc_old_collection_seconds_sum(self, node_name):
        """
        JVM老年代GC用时（秒）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['gc']['collectors']['old']['collection_time_in_millis']
        search_msg = search_msg / 1000
        return search_msg

    def get_elasticsearch_jvm_gc_young_collection_seconds_sum(self, node_name):
        """
        JVM年轻代GC用时（秒）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['gc']['collectors']['young']['collection_time_in_millis']
        search_msg = search_msg / 1000
        return search_msg

    def get_elasticsearch_jvm_memory_max_bytes(self, node_name):
        """
        JVM内存最大值（字节）
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['jvm']['mem']
        return search_msg

    # todo
    def get_elasticsearch_node_stats_up(self):
        pass

    def get_elasticsearch_nodes_roles(self, node_name):
        """
        节点角色
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['roles']
        return search_msg

    def get_elasticsearch_os_cpu_percent(self, node_name):
        """
        OS CPU占用率
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['os']['cpu']['percent']
        return search_msg

    def get_elasticsearch_os_mem_free_bytes(self, node_name):
        """
        空闲物理内存字节数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['os']['mem']['free_in_bytes']
        return search_msg

    def get_elasticsearch_os_mem_used_bytes(self, node_name):
        """
        占用物理内存字节数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['os']['mem']['used_in_bytes']
        return search_msg

    def get_elasticsearch_process_cpu_percent(self, node_name):
        """
        进程cpu占用率
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['process']['cpu']['percent']
        return search_msg

    def get_elasticsearch_process_cpu_time_seconds_sum(self, node_name):
        """
        进程占用cpu时间
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['process']['cpu']['total_in_millis']
        return search_msg

    def get_elasticsearch_process_max_files_descriptors(self, node_name):
        """
        允许打开的最大文件数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['process']['max_file_descriptors']
        return search_msg

    # todo
    def get_elasticsearch_process_mem_resident_size_bytes(self):
        pass

    def get_elasticsearch_process_open_files_count(self, node_name):
        """
        进程打开的文件数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['process']['open_file_descriptors']
        return search_msg

    def get_elasticsearch_transport_rx_packets_total(self, node_name):
        """
        接收的包总数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['transport']['rx_count']
        return search_msg

    def get_elasticsearch_transport_tx_packets_total(self, node_name):
        """
        发送的包总数
        :return:
        """
        cmd = "curl http://{}:{}/_nodes/stats -u{}:{}".format(self.ip, self.port, self.username, self.passwd)
        search_msg = self._run_cmd(cmd)
        search_msg = json.loads(search_msg)
        search_msg = search_msg["nodes"][node_name]['transport']['tx_count']
        return search_msg

    def main(self):
        self.print_usage()
        node_name = self.get_nodes_name()
        # 断路器
        elasticsearch_breakers_accounting_limit_size_bytes_msg = self.get_elasticsearch_breakers_accounting_limit_size_bytes(node_name)
        elasticsearch_breakers_fielddata_limit_size_bytes_msg = self.get_elasticsearch_breakers_fielddata_limit_size_bytes(node_name)
        elasticsearch_breakers_in_flight_requests_limit_size_bytes_msg = self.get_elasticsearch_breakers_in_flight_requests_limit_size_bytes(node_name)
        elasticsearch_breakers_parent_limit_size_bytes_msg = self.get_elasticsearch_breakers_parent_limit_size_bytes(node_name)
        elasticsearch_breakers_request_limit_size_bytes_msg = self.get_elasticsearch_breakers_request_limit_size_bytes(node_name)
        # 集群健康
        elasticsearch_cluster_health_status_msg = self.get_elasticsearch_cluster_health_status()
        # 版本信息
        elasticsearch_clusterinfo_version_info_msg = self.get_elasticsearch_clusterinfo_version_info()
        # 块设备信息
        elasticsearch_filesystem_data_available_bytes_msg = self.get_elasticsearch_filesystem_data_available_bytes(node_name)
        elasticsearch_filesystem_data_free_bytes_msg = self.get_elasticsearch_filesystem_data_free_bytes(node_name)
        elasticsearch_filesystem_data_size_bytes_msg = self.get_elasticsearch_filesystem_data_size_bytes(node_name)
        # indices
        elasticsearch_indices_docs_msg = self.get_elasticsearch_indices_docs()
        elasticsearch_indices_docs_deleted_msg = self.get_elasticsearch_indices_docs_deleted()
        elasticsearch_indices_flush_time_seconds_msg = self.get_elasticsearch_indices_flush_time_seconds()
        elasticsearch_indices_flush_total_msg = self.get_elasticsearch_indices_flush_total()
        elasticsearch_indices_query_miss_count_msg = self.get_elasticsearch_indices_query_miss_count()
        elasticsearch_indices_search_query_time_seconds_msg = self.get_elasticsearch_indices_search_query_time_seconds()
        elasticsearch_indices_search_query_total_msg = self.get_elasticsearch_indices_search_query_total()
        elasticsearch_indices_store_size_bytes_msg = self.get_elasticsearch_indices_store_size_bytes()
        # jvm
        elasticsearch_jvm_buffer_pool_used_bytes_msg = self.get_elasticsearch_jvm_buffer_pool_used_bytes(node_name)
        elasticsearch_jvm_gc_old_collection_seconds_count_msg = self.get_elasticsearch_jvm_gc_old_collection_seconds_count(node_name)
        elasticsearch_jvm_gc_young_collection_seconds_count_msg = self.get_elasticsearch_jvm_gc_young_collection_seconds_count(node_name)
        elasticsearch_jvm_gc_old_collection_seconds_sum_msg = self.get_elasticsearch_jvm_gc_old_collection_seconds_sum(node_name)
        elasticsearch_jvm_gc_young_collection_seconds_sum_msg = self.get_elasticsearch_jvm_gc_young_collection_seconds_sum(node_name)
        elasticsearch_jvm_memory_max_bytes_msg = self.get_elasticsearch_jvm_memory_max_bytes(node_name)
        # 节点角色
        elasticsearch_nodes_roles_msg = self.get_elasticsearch_nodes_roles(node_name)
        # os
        elasticsearch_os_cpu_percent_msg = self.get_elasticsearch_os_cpu_percent(node_name)
        elasticsearch_os_mem_free_bytes_msg = self.get_elasticsearch_os_mem_free_bytes(node_name)
        elasticsearch_os_mem_used_bytes_msg = self.get_elasticsearch_os_mem_used_bytes(node_name)
        # 进程
        elasticsearch_process_cpu_percent_msg = self.get_elasticsearch_process_cpu_percent(node_name)
        elasticsearch_process_cpu_time_seconds_sum_msg = self.get_elasticsearch_process_cpu_time_seconds_sum(node_name)
        elasticsearch_process_max_files_descriptors_msg = self.get_elasticsearch_process_max_files_descriptors(node_name)
        elasticsearch_process_open_files_count_msg = self.get_elasticsearch_process_open_files_count(node_name)
        # transport
        elasticsearch_transport_rx_packets_total_msg = self.get_elasticsearch_transport_rx_packets_total(node_name)
        elasticsearch_transport_tx_packets_total_msg = self.get_elasticsearch_transport_tx_packets_total(node_name)

        elasticsearch_msg_dict = {
            "elasticsearch_breakers_accounting_limit_size_bytes": elasticsearch_breakers_accounting_limit_size_bytes_msg,
            "elasticsearch_breakers_fielddata_limit_size_bytes": elasticsearch_breakers_fielddata_limit_size_bytes_msg,
            "elasticsearch_breakers_in_flight_requests_limit_size_bytes": elasticsearch_breakers_in_flight_requests_limit_size_bytes_msg,
            "elasticsearch_breakers_parent_limit_size_bytes": elasticsearch_breakers_parent_limit_size_bytes_msg,
            "elasticsearch_breakers_request_limit_size_bytes": elasticsearch_breakers_request_limit_size_bytes_msg,
            "elasticsearch_cluster_health_status": elasticsearch_cluster_health_status_msg,
            "elasticsearch_clusterinfo_version_info": elasticsearch_clusterinfo_version_info_msg,
            "elasticsearch_filesystem_data_available_bytes": elasticsearch_filesystem_data_available_bytes_msg,
            "elasticsearch_filesystem_data_free_bytes": elasticsearch_filesystem_data_free_bytes_msg,
            "elasticsearch_filesystem_data_size_bytes": elasticsearch_filesystem_data_size_bytes_msg,
            "elasticsearch_indices_docs": elasticsearch_indices_docs_msg,
            "elasticsearch_indices_docs_deleted": elasticsearch_indices_docs_deleted_msg,
            "elasticsearch_indices_flush_time_seconds": elasticsearch_indices_flush_time_seconds_msg,
            "elasticsearch_indices_flush_total": elasticsearch_indices_flush_total_msg,
            "elasticsearch_indices_query_miss_count": elasticsearch_indices_query_miss_count_msg,
            "elasticsearch_indices_search_query_time_seconds": elasticsearch_indices_search_query_time_seconds_msg,
            "elasticsearch_indices_search_query_total": elasticsearch_indices_search_query_total_msg,
            "elasticsearch_indices_store_size_bytes": elasticsearch_indices_store_size_bytes_msg,
            "elasticsearch_jvm_buffer_pool_used_bytes": elasticsearch_jvm_buffer_pool_used_bytes_msg,
            "elasticsearch_jvm_gc_old_collection_seconds_count": elasticsearch_jvm_gc_old_collection_seconds_count_msg,
            "elasticsearch_jvm_gc_young_collection_seconds_count": elasticsearch_jvm_gc_young_collection_seconds_count_msg,
            "elasticsearch_jvm_gc_old_collection_seconds_sum": elasticsearch_jvm_gc_old_collection_seconds_sum_msg,
            "elasticsearch_jvm_gc_young_collection_seconds_sum": elasticsearch_jvm_gc_young_collection_seconds_sum_msg,
            "elasticsearch_jvm_memory_max_bytes": elasticsearch_jvm_memory_max_bytes_msg,
            "elasticsearch_nodes_roles": elasticsearch_nodes_roles_msg,
            "elasticsearch_os_cpu_percent": elasticsearch_os_cpu_percent_msg,
            "elasticsearch_os_mem_free_bytes": elasticsearch_os_mem_free_bytes_msg,
            "elasticsearch_os_mem_used_bytes": elasticsearch_os_mem_used_bytes_msg,
            "elasticsearch_process_cpu_percent": elasticsearch_process_cpu_percent_msg,
            "elasticsearch_process_cpu_time_seconds_sum": elasticsearch_process_cpu_time_seconds_sum_msg,
            "elasticsearch_process_max_files_descriptors": elasticsearch_process_max_files_descriptors_msg,
            "elasticsearch_process_open_files_count": elasticsearch_process_open_files_count_msg,
            "elasticsearch_transport_rx_packets_total": elasticsearch_transport_rx_packets_total_msg,
            "elasticsearch_transport_tx_packets_total": elasticsearch_transport_tx_packets_total_msg,

        }
        elasticsearch_msg_json = json.dumps(elasticsearch_msg_dict)
        print(elasticsearch_msg_json)
        return elasticsearch_msg_json

if __name__ == '__main__':
    ElasticsearchCollect().main()




