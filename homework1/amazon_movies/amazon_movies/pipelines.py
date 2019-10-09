# -*- coding: utf-8 -*-

class AmazonMoviesPipeline(object):
    def process_item(self, item, spider):
        if not item['validation']:
            return
        with open('found.txt', 'a') as file:
            file.write(item['ID']+'\n')
        with open('results.txt', 'a') as file:
            for key, value in item.items():
                if key == 'meta_info':
                    for k, v in value.items():
                        if v.strip() == '':
                            continue
                        file.write(k.strip().replace(':','') + ': ' 
                        + v.strip().replace(':','') + '\n')
                elif key == 'validation':
                    continue
                elif value.strip() == '':
                        continue
                else:
                    file.write(key.strip().replace(':','') + ': ' 
                    + value.strip().replace(':','') + '\n')
            file.write('\n')
