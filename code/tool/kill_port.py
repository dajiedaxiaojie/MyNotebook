import subprocess
import sys

def find_pid_by_port(port):
    try:
        if sys.platform == "win32":
            # Windows 系统
            result = subprocess.run(
                ["netstat", "-ano", "|", "findstr", f":{port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                pids = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        pids.append(parts[-1])
                return pids
        else:
            # Linux/macOS 系统
            result = subprocess.run(
                ["lsof", "-i", f":{port}", "-t"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split()
        return []
    except Exception as e:
        print(f"查找端口 {port} 的 PID 时出错: {e}")
        return []

def kill_process_by_pid(pids):
    for pid in pids:
        try:
            if sys.platform == "win32":
                # Windows 系统
                subprocess.run(["taskkill", "/PID", pid, "/F"], check=True)
            else:
                # Linux/macOS 系统
                subprocess.run(["kill", "-9", pid], check=True)
            print(f"已终止进程 {pid}")
        except Exception as e:
            print(f"终止进程 {pid} 时出错: {e}")

if __name__ == '__main__':
    # 示例：查找并终止占用端口 8080 的进程
    port = 8000
    pids = find_pid_by_port(port)
    if pids:
        print(f"占用端口 {port} 的 PID: {', '.join(pids)}")
        kill_process_by_pid(pids)
    else:
        print(f"端口 {port} 未被占用")