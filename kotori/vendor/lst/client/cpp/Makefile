# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>

name     := udp_sender

#compiler := /usr/bin/clang++
#compiler := /usr/bin/g++
compiler := /opt/local/bin/g++-mp-5
cppflags := -std=c++11
define INCLUDE
	-I.
endef

source   := $(name).cpp
elf      := $(name)

all: elf run

elf:
	@$(compiler) $(cppflags) $(INCLUDE) -o $(elf) udp.cpp $(source)

run:
	@./$(elf)


server:
	socat -x udp-listen:8888 stdout
