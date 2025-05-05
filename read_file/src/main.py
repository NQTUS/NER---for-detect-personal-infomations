from file_processor import process_file

if __name__ == "__main__":
    file_path = r"C:\MaHoa\read_file\test_files\test_doc.doc"
    file = process_file(file_path)
    print(file)