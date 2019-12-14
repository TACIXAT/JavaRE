from class_classes import File, FileInterface
import argparse 

def main():
    parser = argparse.ArgumentParser(
        description='Dump file information for Java class files.')
    parser.add_argument(
        '--file',
        metavar='file.class',
        type=str,
        help='class file to be dumped',
        required=True)
    parser.add_argument(
        '--no-print',
        action='store_true',
        default=False,
        help='do not pretty print the module contents')
    args = parser.parse_args()

    with open(args.file, 'rb+') as in_file:
        file_interface = FileInterface(in_file.read())

    cf = File(file_interface)

    if not args.no_print:
        cf.pretty_print()

if __name__ == '__main__':
	main()