import argparse
import os

from src.service.markdown_file_service import MarkdownFileService
from src.service.markdown_text_service import MarkdownTextService
from src.service.s3_service import S3Service


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="path to Markdown file", required=True)
    parser.add_argument("--url", "-u", help="S2 or CloudFront domain name", required=True)
    parser.add_argument("--bucket", "-b", help="S3 bucket name", required=True)
    parser.add_argument("--root", "-r", help="Project root path", default="", required=False)
    args = parser.parse_args()
    args_file = args.file
    args_aws_domain_name = args.url
    bucket = args.bucket
    project_root_path = args.root
    # Change directory
    os.chdir(os.path.dirname(args_file))

    markdown_file_service: MarkdownFileService = MarkdownFileService(args_file)

    try:
        markdown_string: str = markdown_file_service.open_markdown()
        markdown_text_service: MarkdownTextService = MarkdownTextService(markdown_string)
    except FileNotFoundError:
        raise Exception("Markdown file is not fount")

    # Upload to S3
    s3_service = S3Service(bucket)
    for file in markdown_text_service.markdown_image_file_list:
        s3_service.upload_file(file.get_path(project_root_path))

    # Replace Markdown image file path
    replaced_string: str = markdown_text_service.replace_markdown_image_file_path(args_aws_domain_name)
    markdown_file_service.save_markdown(replaced_string)


if __name__ == '__main__':
    main()
