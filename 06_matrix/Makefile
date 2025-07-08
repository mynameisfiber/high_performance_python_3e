SCRIPTS  := $(sort $(filter-out _%.py, $(wildcard *.py)))
PERF     := $(patsubst %.py, perf/%.perf, $(SCRIPTS))
TIME     := $(patsubst %.py, time/%.time, $(SCRIPTS))
MEMIT    := $(patsubst %.py, memit/%.memit, $(SCRIPTS))
KERNPROF := $(patsubst %.py, kernprof/%.kernprof, $(SCRIPTS))

all: $(PERF) $(TIME) $(MEMIT) $(KERNPROF)

perf: $(PERF)

time: $(TIME)

memit: $(MEMIT)

kernprof: $(KERNPROF)

kernprof/%.kernprof: %.py
	@echo "lineprof-izing $<"
	mkdir -p kernprof || true
	nice -n -20 kernprof -l -v $< > $@ 2>&1

memit/%.memit: %.py
	@echo "%memit-izing $<"
	mkdir -p memit || true
	nice -n -20 python -m memory_profiler $< > $@ 2>&1

time/%.time: %.py
	@echo "Timing $<"
	mkdir -p time || true
	time -v python $< > $@ 2>&1

perf/%.perf: %.py
	@echo "Perfiling $<"
	mkdir -p perf || true
	@nice -n -20 perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,page-faults,minor-faults,cs,migrations python $< 2>&1 | sed 's/(\([0-9.]*%\))//g' > $@
	@grep 'seconds time' $@ | column -t | cut -f1 -d' '
	@grep 'cache-misses' $@ | column -t
	@grep 'migrations' $@ | column -t
	@echo ''

clean:
	rm -rf perf/ time/ memit/ kernprof/
