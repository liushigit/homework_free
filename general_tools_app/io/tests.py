from general_tools_app.io.dir_tools import *

def test_1():
        for i in list_files_with_ext(u'E:/TDDOWNLOAD/cubase4/Hummel vol. 1', 'jpg'):
            print i

def test_2():
    print list_fn_between('2009.01.02', '2009.01.23', 
                          '/Users/shiliu/Documents/test', 'cn')

def test_sha():
    print md5_of_dir_by_filenames('/Volumes/UPASS/Music/Bee/Repin')


if __name__ == '__main__':
	import sys, getopt, os

	myopts, args = getopt.getopt(sys.argv[1:], 'i:d:e:')

	for option, arg in myopts:
	    if option == '-i':
	        top = arg
	    if option == '-d':
	    	dst = arg
	    if option == '-e':
	    	ext = arg
	compress_sub_dirs(top, dst, '', ext)


# compress_sub_dirs('/Users/shiliu/_code/sites/myapp/views', 
#                   '/Users/shiliu/')

# tar_dir('/Users/shiliu/_code/GitHub', 
#         '/Users/shiliu/_code/zz.tar.gz',
#         '/Users')

# tar_dir('/home/FtpData/liushie/10000309', 
#         '/home/FtpData/liushie/zz.tar.gz')

# print find_top_dir('/Users/shiliu/_code/tools')
# print find_top_dir('/Users/shiliu/_code/notes')
# print find_top_dir('/Users/shiliu/_code/sites')

# for i in gen_sub_dirs('/Users/shiliu/_code/sites/myapp/views'):
#     print i
# print os.path.commonprefix(sub_dir_list('/Users/shiliu/_code/sites/myapp/views'))
