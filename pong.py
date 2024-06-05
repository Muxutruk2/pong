#!/usr/bin/env python3

"""
This script provides a Python CLI alternative to the ping command.

Usage:
    python ping_cli.py [OPTIONS] HOST

Options:
  -c, --count INTEGER      Number of packets to send.  [default: 4]
  -i, --interval INTEGER   Interval between packets (seconds).  [default: 1]
  -t, --timeout INTEGER    Timeout in seconds.  [default: 1]
  -s, --size INTEGER       Size of each packet (bytes).  [default: 56]
  --infinite               Ping the host infinitely.

Arguments:
  HOST                      The host to ping.

Example:
    python ping_cli.py google.com -c 10 -i 0.5
"""

import click
from pythonping import ping, executor
from time import sleep
from datetime import datetime
from rich.console import Console
from rich.table import Table
from typing import List

def format_color(value: float, thresholds: List[float], append: str) -> str:
    """
    Format the value with color based on thresholds.
    """
    if value < thresholds[0]:
        return f"[green]{value}{append}[/green]"
    elif value < thresholds[1]:
        return f"[yellow]{value}{append}[/yellow]"
    else:
        return f"[red]{value}{append}[/red]"

def format_rtt(rtt: float) -> str:
    """
    Format RTT with appropriate color.
    """
    return format_color(rtt, [50, 100], "ms")

def ping_host(host: str, count: int, interval: int, timeout: int, size: int) -> executor.ResponseList:
    """
    Ping the host and return ping results.

    Args:
        host (str): The host to ping.
        count (int): Number of packets to send.
        interval (int): Interval between packets (seconds).
        timeout (int): Timeout in seconds.
        size (int): Size of each packet (bytes).

    Returns:
        list: List of ping response objects.
    """
    return ping(host, count=count, interval=interval, timeout=timeout, size=size, verbose=False)

def create_ping_output(response: executor.Response, host: str, size: int) -> str:
    """
    Create ping output message.

    Args:
        response (ping.PingResponse): Ping response object.
        host (str): The host that was pinged.
        size (int): Size of each packet (bytes).

    Returns:
        str: Ping output message.
    """
    if response.success:
        rtt = response.time_elapsed_ms
        return f'{datetime.now().strftime("%H:%M:%S")} - Reply from {host}: bytes={size} time={format_rtt(rtt)}'
    else:
        return f'{datetime.now().strftime("%H:%M:%S")} - Request timed out'

def construct_stats_panel(sent_packets: int, received_packets: int, rtt_min: float, rtt_max: float, rtt_avg: float, loss_percentage: float) -> Table:
    """
    Construct the stats panel.

    Args:
        sent_packets (int): Total packets sent.
        received_packets (int): Total packets received.
        rtt_min (float): Minimum round-trip time.
        rtt_max (float): Maximum round-trip time.
        rtt_avg (float): Average round-trip time.
        loss_percentage (float): Packet loss percentage.

    Returns:
        str: Statistics panel content.
    """
    stats_table = Table(title="Current Stats", show_header=False)
    stats_table.add_column("Stat", width=15)
    stats_table.add_column("Value", width=20)

    loss_text = format_color(loss_percentage, [10, 20], "%")
    rtt_min_text = format_rtt(rtt_min)
    rtt_max_text = format_rtt(rtt_max)
    rtt_avg_text = format_rtt(round(rtt_avg, 2))

    stats_table.add_row("Sent", str(sent_packets))
    stats_table.add_row("Received", str(received_packets))
    stats_table.add_row("Loss", loss_text)
    stats_table.add_row("RTT Min", rtt_min_text)
    stats_table.add_row("RTT Max", rtt_max_text)
    stats_table.add_row("RTT Avg", rtt_avg_text)

    return stats_table

@click.command()
@click.argument('host')
@click.option('-c', '--count', default=4, help='Number of packets to send.')
@click.option('-i', '--interval', default=1, help='Interval between packets (seconds).')
@click.option('-t', '--timeout', default=1, help='Timeout in seconds.')
@click.option('-s', '--size', default=56, help='Size of each packet (bytes).')
@click.option('--infinite', is_flag=True, help='Ping the host infinitely.')
def ping_cli(host: str, count: int, interval: int, timeout: int, size: int, infinite: bool) -> None:
    """
    A Python CLI alternative to the ping command.
    """
    console = Console()
    sent_packets = 0
    received_packets = 0
    rtt_min = float('inf')
    rtt_max = 0
    rtt_sum = 0
    pings = []

    try:
        while infinite or sent_packets < count:
            sent_packets += 1
            response_list = ping_host(host, 1, interval, timeout, size)
            response = next(iter(response_list), None)

            if response:
                pings.append(create_ping_output(response, host, size))
                if response.success:
                    rtt = response.time_elapsed_ms
                    received_packets += 1
                    rtt_sum += rtt
                    rtt_min = min(rtt_min, rtt)
                    rtt_max = max(rtt_max, rtt)

            if len(pings) > 20:
                pings.pop(0)

            table = Table(title="", width=console.width, show_header=False)
            table.add_column("Ping Output", justify="left")
            for ping_result in pings:
                table.add_row(ping_result)

            loss_count = sent_packets - received_packets
            loss_percentage = (loss_count / sent_packets) * 100 if sent_packets > 0 else 0
            stats = construct_stats_panel(
                sent_packets, 
                received_packets, 
                rtt_min, rtt_max, 
                rtt_sum / received_packets if received_packets > 0 else 0, 
                loss_percentage)

            console.clear()
            console.print(table)
            console.print(stats)

            if not infinite and sent_packets >= count:
                break

            sleep(interval)

        console.print("\nFinal statistics:", style="bold yellow")
        console.print(stats)

    except KeyboardInterrupt:
        console.print("\nPing interrupted.", style="bold yellow")
        console.print("\nFinal statistics:", style="bold yellow")
        console.print(stats)


if __name__ == '__main__':
    ping_cli()
