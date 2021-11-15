from decoder.decoder_interface import decode_segment, test_path
import subprocess


example_path = "../main.py"

def main():
    print(decode_segment("vid/nature", "00001", "00015", "0"))

if __name__ == "__main__":
    main()
