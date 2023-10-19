from langchain.llms import GPT4All
llm = GPT4All(model="C:/Users/edwight/Documents/mi_docker/lit-gpt/checkpoints/openlm-research/orca-mini-3b.ggmlv3.q4_0.bin")

l= llm("The first man on the moon was ... Let's think step by step")

print(l)