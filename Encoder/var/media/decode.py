import os

os.system( "cat SampleVideo_1280x720_10mb/dash_init_0.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_0_*.m4s) > out/all0.m4s")
os.system( "cat SampleVideo_1280x720_10mb/dash_init_1.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_1_*.m4s) > out/all1.m4s")

#os.system("ffmpeg -i out/all5.m4s -c copy out/Vid5.mp4")
os.system("ffmpeg -i out/all0.m4s -i out/all1.m4s -c:v copy -c:a aac out/all01.mp4")

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