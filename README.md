# FieldLab · Unit tests for work instructions

A rush order arrives after label printing but before the first item enters the carton. Which order gets packed? Replay two interpretations, edit the instruction and test the same arrival again.

[Watch the three-minute browser demo](https://thokchomlolet03-cpu.github.io/fieldlab-procedure-lab/) · [Instructions and provenance](procedure_lab/README.md) · [Evaluation results](procedure_lab/RESULTS.md)

With Python 3.10 or later, run these commands from this directory.

~~~sh
python3 -m unittest discover -s procedure_lab -v
python3 -m procedure_lab.server
~~~

Open http://127.0.0.1:8765/. The curated example runs offline using the Python standard library. Live interpretation additionally requires local Ollama with the pinned Llama 3.2 1B model.

The eight-case fictional evaluation returned zero correct classifications in either arm. The curated example demonstrates the simulator. We have no evidence of real workflow improvement.

This submission exports the text experiment from FieldLab development commit `53b66c7a329471cf5ec15aecac412120766740a2`. The earlier F001 video experiment is separate. The original project source code is MIT-licensed. Third-party tools and model weights are distributed separately under their own terms.
