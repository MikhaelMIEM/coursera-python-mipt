import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        try:
            self.conn = socket.create_connection((ip, port), timeout)
        except socket.error:
            raise ClientError("Can't create connection")

    def put(self, metric_name, value, timestamp=str(int(time.time()))):
        try:
            self.conn.sendall(f"put {metric_name} {value} {timestamp}\n".encode())
            data = self.conn.recv(64)
            data = data.decode()
            self._reply_put_handler(data)
        except socket.timeout:
            raise ClientError("Server do not response (timeout)")
        except socket.error:
            raise ClientError("Connection error")

    def _reply_put_handler(self, data):
        if data == 'error\nwrong command\n\n':
            raise ClientError("Server reject command (wrong command)")
        elif data != 'ok\n\n':
            raise ClientError("Unknown response from server")

    def get(self, metric_name):
        try:
            self.conn.sendall(f"get {metric_name}\n".encode())
            data = self.conn.recv(1024)
            data = data.decode()
            return self._reply_get_handler(data)
        except socket.timeout:
            raise ClientError("Server do not response (timeout)")
        except socket.error:
            raise ClientError("Connection error")

    def _reply_get_handler(self, data):
        try:
            answer_dict = {}
            arguments = self._prepare_arguments(data)
            while arguments != '':
                arguments, current_block = self._separate_arguments_and_first_block(arguments)
                answer_dict = self._add_current_block_to_answer_dict(answer_dict, current_block)
            return answer_dict
        except Exception:
            raise ClientError("Can't process server get response data")

    def _prepare_arguments(self, data):
        return data[2:-2]

    def _separate_arguments_and_first_block(self, arguments):
        arguments = self._delete_newline(arguments)
        current_block = self._substr_until_char(arguments, '\n')
        arguments = self._arguments_without_current_block(arguments, current_block)
        return arguments, current_block

    def _delete_newline(self, data):
        return data[1:]

    def _substr_until_char(self, data, char):
        try:
            separator = data.index(char)
        except ValueError:
            return data
        else:
            return data[:separator]

    def _arguments_without_current_block(self, arguments, current_block):
        return arguments.replace(current_block, '', 1)

    def _add_current_block_to_answer_dict(self, answer_dict, current_block):
        current_block = current_block.split(' ', 1)
        values = current_block[1].split(' ')
        if current_block[0] not in answer_dict:
            answer_dict[current_block[0]] = [tuple(map(self._num, values))[::-1]]
        else:
            answer_dict[current_block[0]].append(tuple(map(self._num, values))[::-1])
        return answer_dict

    def _num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)


if __name__ == "__main__":
    client = Client("localhost", 12345, 2)
    print(client.get('soos'))

