# Decompressor Lambda Function
This sample SAM based Lambda deployment takes an S3 event that references a .zip file, through a Lambda Invoke execution, the file is read by the function which then writes each of the extracted files into a separate S3 bucket on the `decompresed/filename_zip/extracted_files` path.
