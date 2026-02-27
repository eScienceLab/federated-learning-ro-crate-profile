# Federated Learning RO-Crate Profile

*Text in Italics = note or template, remove later*

Version: 0.1  
Permalink: N/A  
License: N/A currently  
Authors:

* Eli Chadwick, <https://orcid.org/0000-0002-0035-6475>

Example metadata file: [JSON-LD](example-fl-crate/ro-crate-metadata.json), [HTML preview](example-fl-crate/ro-crate-preview.html)

## Overview

This profile provides guidance on how to describe federated learning processes using RO-Crate.

Input is decentralized data (i.e. may be different for each client), output is a single model trained on that data

Useful metadata - client sites, partitioning strategy, aggregation strategy, output model, description of input data (e.g. cohort query)

This profile is currently designed for “horizontal” federated learning strategies, where each client site holds the same variables for a different cohort. It does not cover “vertical” strategies, where different clients hold different variables for the same cohort.

*Questions to answer:*

* *how an RO-Crate following this profile is expected to be primarily used – where is it exported from, where is it stored, how is it consumed?*  
  * Inform a recipient of the FL configuration that was used, so that they can reproduce it (minimal)  
  * Enable the FL process to be re-run automatically by providing a standard way to document configuration values (ideal)  
* *What is the scope of the profile? What should be split into other RO-Crates? (e.g. reference to a Workflow RO-Crate which could be hosted on WorkflowHub)*  
  * Builds on Process Run Crate  
  * Focus on enriching process run crate with additional metadata specific to FL  
* *What are the most notable classes/keywords/concepts covered by this profile?*

## Compatibility

This profile is based on RO-Crate 1.2 and aims to be compatible with other profiles used in trusted research environments and workflows, including [Five Safes Crate](https://trefx.uk/5s-crate/) (0.4+) and the [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/) family.

## Inheritance

This profile inherits all the requirements from [Process Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate), a profile designed to capture the execution of one or more computational tools. This ensures consistency in the core metadata structure of the crate.

To summarise this profile as an extension of Process Run Crate: the `CreateAction` represents the learning process, with `object` referencing the training datasets AND the learning configuration, `result` referencing the output model, and `instrument` referencing the FL framework used (e.g. Flower).

## *Example Metadata Document (`ro-crate-metadata.json`)*

Example metadata file: [JSON-LD](example-fl-crate/ro-crate-metadata.json), [HTML preview](example-fl-crate/ro-crate-preview.html).

## Full Specification

### Input data

Each dataset used for training SHOULD be represented by a data entity in the crate. The data itself MAY be access controlled. 

In data entities representing training datasets:

* `@id` SHOULD be a persistent identifier for the dataset  
* `license` SHOULD be included. For public datasets this could be an open licence, for restricted or sensitive datasets this can describe the conditions of access  
* `conformsTo` MAY reference a common data model or phenotype dictionary that data in the dataset follows, e.g. OMOP mapping, GA4GH Phenopackets, Frictionless description  
* `subjectOf` MAY reference a contextual or data entity describing a Data Management Plan for the dataset.  
* If [Croissant](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html) metadata is available for the dataset, *TODO describe how this should be included in the crate*
* *How to describe bias/imbalance? Is there a way to do this in Croissant? *
* *List of variables used/filtering criteria - minimum information needed to succeed in the experiment*
  * *For GDPR - if the dataset has 100 vars but you only need 20, you only get the 20*
  * *Information about variables in the dataset may be available - is this needed?* 

Each entity representing a training dataset MUST be referenced from `object` on the `CreateAction` which describes the training execution (see [Federated Learning Process Execution](#federated-learning-process-execution))

#### Data partitioning strategy

The federated learning process described in the crate is assumed to use a “horizontal” data partitioning strategy.

Future versions of this profile may also support “vertical” data partitioning.

### Federated Learning Tools and Configuration

It is assumed that there is, at minimum, a tool or script that is used to train the model on local data. Depending on the architecture or framework used there may be additional tools or scripts, for example to configure a centralized server or aggregator.

#### Training tool or workflow

The training could be orchestrated and run using a specific federated learning framework (e.g. Flower), a general software tool (e.g. Python), or a computational workflow (e.g. a Nextflow workflow), according to how the learning process is designed.

The relevant tool or workflow MUST be described using a contextual entity in the crate which includes the following properties:

* SHOULD have type `SoftwareApplication`, `SoftwareSourceCode` or `ComputationalWorkflow` (may also have other types)  
* SHOULD include `version` with the version of the framework or application used

That entity MUST be referenced from `instrument` in the `CreateAction` describing the training execution (see [Federated Learning Process Execution](#federated-learning-process-execution)).

If a computational workflow is used, the crate MAY also include further metadata to conform to [Workflow Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/).

#### Training configuration – as files

Where the training is configured using configuration files or scripts, those files SHOULD be included in the crate and described using data entities. 

Those entities SHOULD be referenced from `object` in the `CreateAction` describing the training execution (see [Federated Learning Process Execution](#federated-learning-process-execution)).

#### Training configuration – as environment variables

Configuration that is provided using environment variables should be described using `PropertyValue` entities, as in [Process Run Crate: Representing environment variable settings]([https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#representing-enviroment-variable-settings](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#representing-enviroment-variable-settings))

### Federated Learning Process Execution

It is assumed that the training process will usually be captured as a single `CreateAction`. 

#### Execution of the training process

A `CreateAction` entity MUST be present which describes the execution of the training process using the following properties:

* `instrument` MUST reference the entity which describes the [training tool or workflow] (#training-tool-or-workflow)  
* `object`:  
  * SHOULD reference all the [input datasets](#input-datasets) used for the training  
  * SHOULD reference any [configuration files](#training-configuration-as-files) used by the `instrument`  
* `result`:  
  * MUST reference the entity describing the [output model](#output-model)  
  * MAY reference [performance metrics](#metrics-model-performance) of the model or training process (excluding resource usage)  
* `environment` MAY reference [environmental variables used for configuration](#training-configuration-as-environment-variables)  
* `resourceUsage` MAY reference [resource usage metrics](#metrics-resource-usage) for the training process  
* Other properties (e.g. `name`, `description`, `agent`) SHOULD follow the guidelines set in [Process Run Crate]([https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#requirements](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#requirements)) 

*Register container digests & env lock files for environment capture*

#### Pre-processing and post-processing

Additional `CreateAction`s MAY be included in the crate to describe pre- and post- processing steps. See [Process Run Crate: Multiple processes]([https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#multiple-processes](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/#multiple-processes)).

Note that if those pre- or post-processing steps are part of an automated workflow, they may be sufficiently described by using [Workflow Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) or [Provenance Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/provenance_run_crate/)).

#### Metrics - resource usage

Resource metrics – such as memory usage, execution time, estimated carbon cost, etc. –  MAY be included in the crate. If they are they SHOULD follow the guidance in [Provenance Run Crate: Representing resource usage]([https://www.researchobject.org/workflow-run-crate/profiles/provenance_run_crate/#representing-resource-usage](https://www.researchobject.org/workflow-run-crate/profiles/provenance_run_crate/#representing-resource-usage)).

<!-- note 2026-02-26: this link does not yet work as the material is not yet merged into RDMkit -->  
For guidance on best-practice metrics to collect for federated learning, see [RDMkit: Federated Learning]([https://rdmkit.elixir-europe.org/federated_learning](https://rdmkit.elixir-europe.org/federated_learning)) 

#### Metrics - model performance

Metrics that describe the performance of the training process and/or the trained model – such as drift detection metrics, loss/accuracy metrics, client-participation rate, etc. –  MAY be included in the crate. If included, they SHOULD be described using `PropertyValue` entities, and those entities MUST be linked from `result` on the `CreateAction` (along with the model itself, see [Output model](#output-model))

A `PropertyValue` instance used to represent a performance metric MUST have a unique identifier representing the quantity being measured as its [propertyID](http://schema.org/propertyID), and SHOULD refer to a unit of measurement via [unitCode](http://schema.org/unitCode), except for dimensionless numbers.

This aligns with the guidance on resource usage metrics above, except that the metrics are connected through `result` rather than `resourceUsage`.

<!-- note 2026-02-26: this link does not yet work as the material is not yet merged into RDMkit -->  
For guidance on best-practice metrics to collect for federated learning, see [RDMkit: Federated Learning]([https://rdmkit.elixir-europe.org/federated_learning](https://rdmkit.elixir-europe.org/federated_learning)) 

### Output model

The crate MUST contain a data entity representing the output model. This could be a direct serialisation of the model to file, or another representation of the model. The data entity:

* SHOULD have a persistent identifier as `@id` if such an identifier exists for the model  
* SHOULD have `license` indicating usage conditions for the model; it is RECOMMENDED that an SPDX identifier is used. If no `license` is declared then the `license` from the Root Data Entity is assumed to apply to the model  
* SHOULD declare `encodingFormat` and/or `conformsTo` with the format for the model. See [RO-Crate: Adding detailed descriptions of File encodings]([https://www.researchobject.org/ro-crate/specification/1.2/data-entities.html#adding-detailed-descriptions-of-file-encodings](https://www.researchobject.org/ro-crate/specification/1.2/data-entities.html#adding-detailed-descriptions-of-file-encodings)) and [RO-Crate: File format profiles]([https://www.researchobject.org/ro-crate/specification/1.2/data-entities.html#file-format-profiles](https://www.researchobject.org/ro-crate/specification/1.2/data-entities.html#file-format-profiles)). *Is this sufficient/appropriate? E.g. pickling does not quite match this structure (Python-specific serialization). What about a function that converts model coefficients to a table?*  
* MAY be a web-based data entity which MAY be access-controlled

The model MAY be further documented by one or more supplementary files, such as [Model Cards](https://huggingface.co/docs/hub/model-cards) or [AI Model Passport]([https://arxiv.org/abs/2506.22358](https://arxiv.org/abs/2506.22358)). Where such files are represented as data entities within the crate:

* the model entity MUST reference them through `subjectOf`  
* If the files were automatically generated during/at the end of the training process, the relevant `CreateAction` SHOULD reference them via `result`

### Additional metadata

#### Sensitive Data

In processes where sensitive data is used, the [Five Safes RO-Crate](https://trefx.uk/5s-crate/0.4/) profile MAY additionally be followed.

<!--
## Requirements Table {#requirements-table}

*Including this table helps people using the profile understand quickly if they have met all of the requirements. Group the requirements by the class that they apply to.*

*Class type `Foo`*

| *Property* | *Required* | *Description* |
| :---- | :---- | :---- |
| *name* | *MUST* | *MUST match the name of this entity in Some Other Database* |
| *hasPart* | *SHOULD* | *Referenced entities SHOULD be of type `Bar`* |

*Class type `Bar`*

| *Property* | *Required* | *Description* |
| :---- | :---- | :---- |
| *name* | *MUST* | *MUST match the name of this entity in Some Other Database* |
-->
