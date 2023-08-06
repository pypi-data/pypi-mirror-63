# NLP Annotations

A simple python package for dealing with different nlp annotation styles.
No dependencies, and is very fast due to only using regular expressions.

You can install it with:

```bash
pip3 install nlp-annotations
```

## Annotation Types

The following are the annotation types we support and how to convert it to
another type.

### Markdown Links

(Used by Rasa, etc...), these are in the form:

```markdown
The weather is [sunny](weather) and the sky is [blue](color).
```

To convert this to an _entity list_ you can:

```python
markdown_links2entity_list("The weather is [sunny](weather) and the sky is [blue](color).")
# ('The weather is sunny and the sky is blue.', {'entities': [(15, 20, 'weather'), (36, 40, 'color')]})
```

### Entity List

(Used by Spacy, etc...), these are in the form:

```python
('The weather is sunny and the sky is blue.', {'entities': [(15, 20, 'weather'), (36, 40, 'color')]})
```

To convert this to a _markdown links_ string, you can:

```python
entity_list2markdown_links("The weather is sunny and the sky is blue.", [(15, 20, 'weather'), (36, 40, 'color')])
# 'The weather is [sunny](weather) and the sky is [blue](color).'
```
