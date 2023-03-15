import os
import re
from tqdm.contrib.concurrent import process_map

root = '/mnt/nfs/miyoung/suehyun/cc_wet/2022-49/logs'
URL_PATTERN = r"https:\/\/data\.commoncrawl\.org\/crawl-data\/CC-MAIN-.*\/segments\/\d+\.\d+\/wet\/CC-MAIN-\d+-\d+-\d+\.warc\.wet\.gz"
downloaded = set()

def process_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if 'Downloaded' in line:
                url = re.search(URL_PATTERN, line)
                if url:
                    downloaded.add(url.group())

def process_files_in_parallel(path):
    # Get a list of all .err files in the directory and its subdirectories
    file_paths = [path + '/1554_0_log.err', path + '/1540_0_log.err']
    # for root, dirs, files in os.walk(path):
    #     for file in sorted(files):
    #         if file.endswith('.err'):
    #             file_paths.append(os.path.join(root, file))
    # print(f'From {files[0]} to {files[-1]}')

    # # Use a pool of worker processes to process the files in parallel
    # with Pool(proce) as pool:
    #     # # Use tqdm to create a progress bar and pass it to the process_file() function
    #     # with tqdm(total=len(file_paths), desc='Processing files') as progress_bar:
    #     #     # Use the new function with the Pool object
    #     #     for _ in pool.imap_unordered(process_file, file_paths, chunksize=chunksize):
    #     #         progress_bar.update(1)
    #     pool.map(process_file, file_paths)
    process_map(process_file, file_paths, max_workers=4)


if __name__ == '__main__':
    process_files_in_parallel(root)
    print(len(downloaded))
    # Print the downloaded URLs
    with open('downloaded.txt', 'w') as f:
        for url in downloaded:
            f.write(url + '\n')


