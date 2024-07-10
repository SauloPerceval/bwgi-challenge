import io
import os


def last_lines(file_name, buffer_size=io.DEFAULT_BUFFER_SIZE, code="utf-8"):
    file_size = os.path.getsize(os.path.abspath(file_name))
    remaining_bytes_number_on_file = file_size

    with open(file_name, "rb", buffering=buffer_size) as file_reader:
        remaining_bytes_buffer = b""

        while remaining_bytes_number_on_file:
            number_of_bytes_to_read = min(buffer_size, remaining_bytes_number_on_file)
            remaining_bytes_number_on_file = max(
                remaining_bytes_number_on_file - buffer_size, 0
            )
            file_reader.seek(remaining_bytes_number_on_file)

            bytes_buffer = file_reader.read(number_of_bytes_to_read)

            bytes_buffer = bytes_buffer + remaining_bytes_buffer
            remaining_bytes_buffer = b""

            while bytes_buffer and not remaining_bytes_buffer:
                bytes_buffer, partition_char, line_bytes = bytes_buffer.rpartition(
                    "\n".encode(code)
                )

                if not partition_char and remaining_bytes_number_on_file:
                    remaining_bytes_buffer = line_bytes
                else:
                    yield line_bytes.decode(code) + "\n"


if __name__ == "__main__":
    for line in last_lines("test_file.txt", 124):
        print(line, end="")
