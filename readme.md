## Task 1 Submission

NOTE: All of the below procedures are done only only the non_equal json and commands are valid for this file only.

### Steps to run -

1. Install required packages

```bash
pip install -r requirements.txt
```

2. Populate .env.template file and change the file name to .env

3. Run evaluation.py to get the score and summay of the resume

```bash
python 'src/evaluation.py' [--id ID] [--full FULL] [--export EXPORT]
```

 - --id arg takes the id of the document
 - --full take the bool value if the full scores should be printed
 - --export exports the result for document in a json file with name as the id

To get responses similarity, run - 

```bash
python 'src/get_responses_similarity.py' [--file FILE] [--start START] [--end END]
```

This command by default export the results in a json named similarities_{start}_{end}.json.

There is some misellaneous code in evaluation.py (commented) which can batch process the evaluation asynchronously. This is not used in the final submission.