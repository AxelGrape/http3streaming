import os
def decoder(path, si, ei, quality):
    quality1 = str(int(quality) + 1)

    #rnge = [*range(int(si.lstrip('0')), int(ei.lstrip('0')))]
    chnks = [str(item).zfill(len(ei)) for item in [*range(int(si.lstrip('0')), int(ei.lstrip('0'))+1)]]

    print("remove contents of out? (y/n)")
    #if input() == "y":
    os.system("rm out/*")


#os.system( "cat $(ls -vx sample_video/dash_init_*.m4s) > sampleF.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_*.m4s) >> sampleF.mp4")

    os.system( "cat " + path + "/dash_init_" + quality + ".m4s > out/all" + quality + ".m4s")
    os.system( "cat " + path + "/dash_init_" + quality1 + ".m4s > out/all" + quality1 + ".m4s")
    for c in chnks:
        os.system( "cat $(ls -vx " + path + "/dash_chunk_" + quality + "_"+str(c)+".m4s) >> out/all" + quality + ".m4s")
        os.system( "cat $(ls -vx " + path + "/dash_chunk_" + quality1 + "_"+str(c)+".m4s) >> out/all" + quality1 + ".m4s")




    #os.system( "cat " + path + "/dash_init_" + quality + ".m4s $(ls -vx " + path + "/dash_chunk_" + quality + "_0000[" + si + "-" + ei + "].m4s) > out/all" + quality + ".m4s")
    #os.system( "cat " + path + "/dash_init_" + quality1 + ".m4s $(ls -vx " + path + "/dash_chunk_" + quality1 + "_0000[" + si + "-" + ei + "].m4s) > out/all" + quality1 + ".m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_0.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_0_0000[0-3].m4s) > out/all0.m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_1.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_1_0000[0-3].m4s) > out/all1.m4s")

    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_0.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_0_0000[4-7].m4s) > out/all0_.m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_1.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_1_0000[4-7].m4s) > out/all1_.m4s")

    #os.system("ffmpeg -i out/all5.m4s -c copy out/Vid5.mp4")
    os.system("ffmpeg -i out/all" + quality + ".m4s -i out/all" + quality1 + ".m4s -c:v copy -c:a aac out/vid" + ei + ".mp4")
    #os.system("ffmpeg -i out/all0_.m4s -i out/all1_.m4s -c:v copy -c:a aac out/all01_.mp4")

    print("Play vid? (y/n)")
    if input() == "y":
        os.system("xdg-open out/vid" + ei + ".mp4")

    #os.system("printf \"file '%s'\n\" out/*.mp4 > mylist.txt")
    #os.system("ffmpeg -f concat -i mylist.txt -c copy out/tmp.mp4")
    #os.system("ffmpeg -i out/tmp.mp4 -c copy out/all01.mp4 -y")
    #echo \"y\" | 
    #os.system("xdg-open out/all01.mp4")

def main():
    path = 'SampleVideo_1280x720_10mb'
    startindex = '00001'
    slutindex = '00007'
    quality = '0'
    decoder(path, startindex, slutindex, quality)

if __name__ == "__main__":
    main()

#print("Play vid? (y/n)")
#if input() == "y":
# os.system("xdg-open out/both01_0347.mp4")

#os.system( "cat $(ls -vx sample_video/dash_init_*.m4s) > sampleF.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_*.m4s) >> sampleF.mp4")


#os.system( "cat sample_video/dash_init_0.m4s > sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_0_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_1.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_1_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_2.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_2_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_3.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_3_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_chunk_0_00001.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00002.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00003.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00004.m4s >> sample00.mp4")
#os.system( "cat hbo/dash_chunk_1_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_1_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_2_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_3_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_3_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_4_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_5_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_5_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_6_00001.m4s >> hbo.mp4")