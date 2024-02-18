CC=gcc
#C5=arm-none-linux-gnueabi-gcc
SS=/usr/ensta/pack/simplescalar-3v0d/bin/sslittle-na-sstrix-gcc

all: pagerank pagerank_med.ss pagerank_max.ss pagerank_min.ss

pagerank : main.c examples.h
	$(CC) main.c -o pagerank -g3 -lm -std=c99 -D_MAT_TWITTER

pagerank_med.ss: main.c examples.h
	$(SS) main.c -o pagerank_med.ss  -D_MAT_SIMPLE


pagerank_max.ss: main.c examples.h
	$(SS) main.c -o pagerank_max.ss  -D_MAT_TWITTER

pagerank_min.ss: main.c examples.h
	$(SS) main.c -o pagerank_min.ss  -D_MAT_EXAMPLE3

#pagerank_basic.out:
#	$(C5) main.c -o pagerank_basic.out -D_MAT_TWITTER -static -O3 -march=armv7-a	-mtune=cortex-a9 -fno-tree-vectorize -mcpu=cortex-a9 -mfloat-abi=soft

#pagerank_fpu.out:
#	$(C5) main.c -o pagerank_fpu.out -D_MAT_TWITTER  -static -O3 -march=armv7-a	-mtune=cortex-a9 -fno-tree-vectorize -mcpu=cortex-a9 -mfloat-abi=softfp	-mfpu=neon

clean : 
	rm pagerank pagerank_*.ss pagerank*out
