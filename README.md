# Pong

Pong is a Python CLI tool that provides an alternative to the `ping` command, with additional features such as colorful output, real-time statistics, and customizable options.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Muxutruk2/pong.git
   ```

2. Navigate to the project directory:
   ```bash
   cd pong
   ```

3. Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Make the script executable:
   ```bash
   chmod +x pong.py
   ```

5. Copy the script to `/usr/local/bin` for global access:
   ```bash
   sudo cp pong.py /usr/local/bin/pong
   ```

6. (Optional) If you want to execute it without the root user, you need to grant the necessary permissions to Python:
   ```bash
   sudo setcap cap_net_raw+ep $(readlink -f $(which python3))
   ```
   Note: This command grants the capability to create packets to any Python program. Use it with caution.

7. (Optional) Create an alias in your shell's configuration file for easier access:
   ```bash
   echo "alias pong='pong'" >> ~/.bashrc
   ```
   Replace `~/.bashrc` with the appropriate configuration file for your shell if you are not using Bash.

## Usage

After installation, you can use `pong` just like the `ping` command:

```bash
pong google.com
```

Additional options can be specified:

- `-c`, `--count`: Number of packets to send.
- `-i`, `--interval`: Interval between packets (in seconds).
- `-t`, `--timeout`: Timeout in seconds.
- `-s`, `--size`: Size of each packet (in bytes).
- `--infinite`: Ping the host infinitely.

Example:
```bash
pong google.com -c 10 -i 0.5
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
