# -*- coding: utf-8 -*-
"""
Ferramenta Universal de Título - Python 3.6+
Apenas para linha de comando do Windows.
"""

from __future__ import print_function
import argparse
import ctypes
import os
import subprocess
import sys
import time

if os.name != "nt":
    print("ERRO: este programa funciona somente no Windows.")
    sys.exit(1)

from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)

EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]
user32.EnumWindows.restype = wintypes.BOOL
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.IsWindowVisible.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.SetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
user32.SetWindowTextW.restype = wintypes.BOOL

def windows_for_pid(pid):
    result = []
    @EnumWindowsProc
    def callback(hwnd, lparam):
        window_pid = wintypes.DWORD(0)
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
        if window_pid.value == pid and user32.IsWindowVisible(hwnd):
            result.append(hwnd)
        return True
    user32.EnumWindows(callback, 0)
    return result

def set_title_for_pid(pid, title):
    changed = 0
    for hwnd in windows_for_pid(pid):
        if user32.SetWindowTextW(hwnd, title):
            changed += 1
    return changed

def run_test(exe, title, interval):
    exe = os.path.abspath(exe)
    if not os.path.isfile(exe):
        print("ERRO: EXE não encontrado:", exe)
        return 2

    print("==============================================")
    print(" MODO TESTE (Em Memória)")
    print("==============================================")
    try:
        process = subprocess.Popen([exe], cwd=os.path.dirname(exe))
    except Exception as exc:
        print("ERRO ao iniciar o aplicativo:", exc)
        return 1

    print("PID do Processo:", process.pid)
    print("Monitorando a janela... Pressione CTRL+C para encerrar o monitor.")
    
    try:
        while process.poll() is None:
            set_title_for_pid(process.pid, title)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido. O app continuará aberto.")
    return 0

def replace_string_universal(data, old_title, new_title):
    """Tenta substituir a string em múltiplas codificações comuns em arquivos PE."""
    encodings = ["utf-16le", "utf-8", "ascii"]
    modified_data = bytearray(data)
    total_changes = 0

    for enc in encodings:
        try:
            old_bytes = old_title.encode(enc)
            new_bytes = new_title.encode(enc)
        except UnicodeEncodeError:
            continue

        if len(new_bytes) > len(old_bytes):
            continue  # Pula se o novo título for maior que o espaço disponível

        # Preenche o espaço restante com bytes nulos apropriados para a codificação
        padding_byte = b"\x00\x00" if enc == "utf-16le" else b"\x00"
        rem = len(old_bytes) - len(new_bytes)
        
        if enc == "utf-16le":
            replacement = new_bytes + (b"\x00\x00" * (rem // 2))
        else:
            replacement = new_bytes + (b"\x00" * rem)

        start = 0
        while True:
            pos = modified_data.find(old_bytes, start)
            if pos < 0:
                break
            
            modified_data[pos:pos + len(old_bytes)] = replacement
            total_changes += 1
            start = pos + len(old_bytes)

    return bytes(modified_data), total_changes

def save_exe(input_exe, title, output_exe, old_title):
    input_exe = os.path.abspath(input_exe)
    output_exe = os.path.abspath(output_exe)

    if not os.path.isfile(input_exe):
        print("ERRO: EXE original não encontrado.")
        return 2

    if os.path.normcase(input_exe) == os.path.normcase(output_exe):
        print("ERRO: O arquivo original não pode ser sobrescrito diretamente.")
        return 2

    try:
        with open(input_exe, "rb") as f:
            original = f.read()
    except IOError as exc:
        print("ERRO ao ler o arquivo:", exc)
        return 1

    modified, count = replace_string_universal(original, old_title, title)

    if count == 0:
        print("ERRO: O texto original não foi encontrado dentro do EXE.")
        print("Certifique-se de que digitou o texto antigo EXATAMENTE como ele é.")
        return 4

    try:
        with open(output_exe, "wb") as f:
            f.write(modified)
    except IOError as exc:
        print("ERRO ao salvar o novo arquivo:", exc)
        return 1

    print("==============================================")
    print(" SALVAR - Executável Modificado com Sucesso!")
    print("==============================================")
    print("Arquivo gerado:", output_exe)
    print("Substituições realizadas:", count)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Altera o título de janelas de arquivos executáveis.")
    sub = parser.add_subparsers(dest="mode")

    test = sub.add_parser("test", help="Altera em tempo de execução (memória)")
    test.add_argument("exe")
    test.add_argument("title")
    test.add_argument("--interval", type=float, default=0.3)

    save = sub.add_parser("save", help="Grava permanentemente em um novo EXE")
    save.add_argument("exe")
    save.add_argument("title")
    save.add_argument("-o", "--output")
    save.add_argument("--old-title", required=True, help="O título atual exato gravado no app")

    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return 2

    if args.mode == "test":
        return run_test(args.exe, args.title, args.interval)

    output = args.output
    if not output:
        base, ext = os.path.splitext(args.exe)
        output = base + "_modificado" + ext

    return save_exe(args.exe, args.title, output, args.old_title)

if __name__ == "__main__":
    sys.exit(main())
