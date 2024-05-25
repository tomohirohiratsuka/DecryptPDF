import os
import subprocess
from dotenv import load_dotenv
import argparse


def decrypt_pdfs(directory):
	# .envファイルから環境変数を読み込む
	load_dotenv()
	password = os.getenv('PDF_PASSWORD')
	if not password:
		print('Error: PDF_PASSWORD environment variable is not set.')
		return

	# decryptedディレクトリを作成
	decrypted_dir = os.path.join(directory, 'decrypted')
	os.makedirs(decrypted_dir, exist_ok=True)

	# ディレクトリ内のすべてのPDFファイルを取得
	for filename in os.listdir(directory):
		if filename.endswith('.pdf'):
			input_path = os.path.join(directory, filename)
			output_path = os.path.join(decrypted_dir, filename)

			# qpdfコマンドを実行してPDFのパスワードを解除
			command = ['qpdf', '--decrypt', '--password={}'.format(password), input_path, output_path]
			try:
				subprocess.run(command, check=True)
				print(f'Successfully decrypted {filename}')
			except subprocess.CalledProcessError:
				print(f'Failed to decrypt {filename}')


if __name__ == '__main__':
	# コマンドライン引数を解析
	parser = argparse.ArgumentParser(description='Decrypt PDF files in a specified directory.')
	parser.add_argument('directory', type=str, help='The directory containing the PDF files to decrypt')
	args = parser.parse_args()

	# 指定されたディレクトリで関数を呼び出し
	decrypt_pdfs(args.directory)
