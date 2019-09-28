# -*- coding: utf-8 -*-

class AmazonMoviesPipeline(object):
    def process_item(self, item, spider):
        if not item['validation']:
            return
        with open('results/results.txt', 'a') as file:
            for key, value in item.items():
                if key == 'meta_info':
                    for k, v in value.items():
                        file.write(k.strip().replace(':','') + ': ' 
                        + v.strip().replace(':','') + '\n')
                elif key == 'validation':
                    continue
                else:
                    file.write(key.strip().replace(':','') + ': ' 
                    + value.strip().replace(':','') + '\n')
            file.write('\n')
