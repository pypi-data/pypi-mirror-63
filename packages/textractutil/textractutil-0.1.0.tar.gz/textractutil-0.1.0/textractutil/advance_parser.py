from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from collections import defaultdict

from .response_parser import Document

class Parsed_Document(Document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_text_blocks(self):
		"""
		Get all text blocks in a Textract response.
		|
		| Output: dict{int: list[string]}
		|    key: page number
		|    value: list of text phrases
		"""
		res = defaultdict(list)

		for index, page in enumerate(self._pages, start=1):
			for block in page.blocks:
				if block.get("BlockType", "") == "LINE":
					if "Text" in block: 
						res[index].append(block["Text"])

		return res

	def get_text(self):
		"""
		Get text in a Textract response.
		|
		| Output: dict{int: string}
		|    key: page number
		|    value: text
		"""
		temp_res = self.get_text_blocks()

		res = defaultdict(lambda:"")
		res.update({k:" ".join(v) for k, v in temp_res.items()})

		return res

	def get_text_blocks_by_row(self):
		"""
		Get all text blocks in a Textract response by row.
		|
		| Output: dict{int: list[list[string]]}
		|    key: page number
		|    value: list of list of text phrases
		"""
		res = defaultdict(list)

		for index, page in enumerate(self._pages, start=1):
			cur_left, cur_row = 0, []
			for block in page.blocks:
				block_left = block.get("Geometry", {}).get("BoundingBox", {}).get("Left", None)
				block_type = block.get("BlockType", "")
				block_text = block.get("Text", "")
				if block_left is None or block_type != "LINE": 
					continue
				elif block_left < cur_left:
					if cur_row: res[index].append(cur_row)
					cur_left, cur_row = block_left, [block_text] if block_text else []
				else:
					cur_left = block_left
					if block_text: cur_row.append(block_text)
			if cur_row: res[index].append(cur_row)

		return res

	def get_text_by_row(self):
		"""
		Get text in a Textract response by row.
		|
		| Output: dict{int: list[string]}
		|    key: page number
		|    value: list of string
		"""
		temp_res = self.get_text_blocks_by_row()

		res = defaultdict(list)
		res.update({k:[" ".join(i) for i in v] for k, v in temp_res.items()})

		return res

	def get_form(self):
		"""
		Get extracted key value pairs from Textract response.
		|
		| Output: dict{int: list(tuple)}
		|    key: page number
		|    value: list of key value pair in tuple
		"""
		res = defaultdict(list)

		for index, page in enumerate(self._pages, start=1):
			fields = [(i.key._text ,i.value._text if i.value else None, i.key.geometry.boundingBox.top) for i in page.form.fields]
			res[index] = [(i[0], i[1]) for i in sorted(fields, key=lambda x: x[-1])]

		return res 

	def get_table(self):
		"""
		Get extracted tables from Textract response.
		|
		| Output: dict{int: list(tuple)}
		|    key: page number
		|    value: dict{tuple:string}
		|        key: (row_number, col_number)
		|        value: cell text
		"""
		res = defaultdict(dict)

		for index, page in enumerate(self._pages, start=1):
			for table in page.tables:
				for r, row, in enumerate(table.rows, start=1):
					for c, cell in enumerate(row.cells, start=1):
						res[(r,c)] = cell.text

		return res 

