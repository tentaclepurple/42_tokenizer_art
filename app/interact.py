import subprocess


def run_js_script(script_name, token_uri=None):
   try:
       command = f"TOKEN_URI={token_uri} npx hardhat run {script_name} --network amoy"
       result = subprocess.run(command, shell=True, cwd='/app', capture_output=True, text=True)
       print("Stdout:", result.stdout)
       print("Stderr:", result.stderr)
       return result.stdout
   except Exception as e:
       print(f"Error: {e}")
       return None


def main():
    token_uri = 'ipfs://bafybeiecl7myvuveviqzi3lrpy2r3i5ijkdhkunimyc6gyzrrcck7c375m'

    run_js_script('deployment/getTokenURIs.js')


if __name__ == "__main__":
    main()
