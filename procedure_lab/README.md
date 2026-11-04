# Unit Tests for Work Instructions

A rush order arrives after a regular order's label has printed but before its first item enters the carton. Should the worker finish the regular order or switch? FieldLab turns each candidate meaning of “packing has started” into a rule and shows the resulting action. A supervisor can define the boundary and replay the same arrival.

## Launch

From the repository root run:

```sh
python3 -m procedure_lab.server
```

Open [the local test bench](http://127.0.0.1:8765/). Python 3.10+ supports the simulator and server. The app binds to loopback. Its default curated mode works immediately with the opening procedure and the two offered repairs.

For live text interpretation, start local Ollama and use the pinned Meta Llama 3.2 1B package installed for this experiment. On a new machine, obtaining the model requires a download.

```sh
ollama pull llama3.2:1b
python3 -c "from procedure_lab.model import status; print(status('llama3.2:1b'))"
```

Select **Local Meta model**, type an instruction and click **Run procedure test**. This path makes a local Ollama chat request. It checks the manifest digest, response structure and verbatim source excerpts. Each accepted reading goes through the same simulator as the curated example. Missing runtimes, rejected outputs and abstentions appear explicitly. The interface keeps input in the page for the current session. The evaluation runner separately saves requests and responses for its fictional inputs.

## Demo in under a minute

1. Read the opening instruction. With the rush order arriving after label printing, the label-start reading returns **regular** and the item-start reading returns **rush**.
2. Choose **At first item placement**. The middle case now returns **rush**.
3. Click **After first item placement**. That later arrival returns **regular**.
4. Restore the original example and try the same instruction in local model mode. Inspect its actual output. Trying a fresh paraphrase tests whether the model translation works beyond the curated example.

The replay explores four event prefixes in a fixed order, including the control after the regular order is complete. It finds a shortest divergence **within this event space and the supplied readings**. A matched quote demonstrates that the words occur in the input. A human reviewer still has to assess whether those words support the proposed interpretation.

## Reproduce the experiment

```sh
python3 -m unittest procedure_lab.test_engine -v
python3 -m procedure_lab.evaluate runs/fresh-procedure-evaluation
```

The evaluation requires local inference. Use a fresh output directory. The runner preserves errors and rejected responses. The frozen deck and scoring rules are in [EVALUATION.md](EVALUATION.md). The historical F001 video tests measure a separate implementation.

## Provenance

The text experiment was implemented on November 3, 2026 on a branch based on the preserved F001 main commit. Its UI, packing simulator, fixture deck and evaluation are new AI-assisted code and data for this experiment. Ollama and Meta Llama are third-party dependencies. Model weights stay in the local Ollama store. Sponsor eligibility of this particular model and the participant submission format require checking against the participant rules.

[Measured results and failure analysis](RESULTS.md) cover the eight-case comparison, the four repair requests and the separately exercised opening rule.
