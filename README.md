# Basic-AI

## What is this project about?

This project tests whether small datasets can be used to train CNN and AI models effectively. I use image augmentation to see which level of image variation affects the final result. To show that this can be done on my own principles, the project uses only open data from NASA and ESO, so no one's work is used without permission.

## The problem

AI models are often trained on large datasets to improve performance and generalization. This practice leads to work by human artists and writers being stolen by corporations. This project tries to address this issue in two ways.

1. I only use open, publicly available NASA and ESO images.

2. I use augmentation (changing the existing images to create more variety) to make a small dataset generate a larger amount of useful data, then test the results against benchmarks to see how the final result is affected.

## Features

- Easily understandable website with an interactive augmentation viewer and a results chart
- Replicable: every factor is trained from a fresh copy of the base images, with a fixed randoms seed.
- Open data only (NASA public domain and ESO CC BY 4.0), with a source, license and credit recorded for every image.
- Runs on a CPU, no GPU needed
- Cross platform

## Usage/Examples

Each factor must be run separately. Copy the base images fresh, augment them at that factor, then train and test:

```bash
python augment.py [ARGUMENTS]
python main.py [ARGUMENTS]
```

results.csv feeds the results chart on the website:

```bash
factor,class,mean_recall,min_recall,max_recall
0,Overall,50.9,48.5,52.0
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/Pratyush-M-code/Basic-AI
```

Go to the project directory

```bash
  cd Basic-AI
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the code!!!

## Deployment

The website is plain HTML, CSS and JavaScript with no build step, so it can be hosted on any static host such as GitHub Pages. Live demo: [https://pratyush-m-code.github.io/Basic-AI/]

## FAQ

### Where do I get the dataset?

This dataset (a training file and a test file) and dataset_sources_combined.csv, which lists the source, license and credit for every image, are at [ZENODO-DOI].

## Acknowledgements

- NASA public domain images (JPL, Goddard, Hubble) and ESO images under CC BY 4.0. Credits for each image are in dataset_sources_combined.csv.
- Pixelify Sans and IBM Plex Mono. Icons: Font Awesome.
- Built for Stardance by Hack Club.
- [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
- [Awesome README](https://github.com/matiassingers/awesome-readme)
- [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
