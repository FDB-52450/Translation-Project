# Este archivo tendra como objetivo agrupar los textos obtenidos por cleanup.py
# en lineas y bloques de texto, para luego ser procesados por el modelo de lenguaje.

from src.models.processing import LineBlock, NormalizedLine, TextBlock

def group_lines_into_blocks(lines: list[NormalizedLine]) -> list[LineBlock]:
	margin_y = 10
	margin_x = 50

	blocks: list[LineBlock] = []
	current_block = None
	previous_line = None

	for line in lines:
		if previous_line:
			prev_line_right_side = previous_line.center_x + previous_line.width / 2
			current_line_left_side = line.center_x - line.width / 2

			if abs(previous_line.center_y - line.center_y) < margin_y and current_line_left_side - prev_line_right_side <= margin_x:
				current_block.lines.append(line)
			else:
				blocks.append(current_block)
				current_block = LineBlock([line])
		else:
			current_block = LineBlock([line])

		previous_line = line

	if current_block:
		blocks.append(current_block)

	return blocks

def group_blocks_into_text_blocks(blocks: list[LineBlock]) -> list[TextBlock]:
	margin_y = 60
	margin_x = 30

	text_blocks: list[TextBlock] = []

	for block in blocks:
		if len(text_blocks) > 0:
			corresponding_block = next((b for b in text_blocks if abs(b.center_y - block.center_y) < margin_y and abs(b.center_x - block.center_x) < margin_x), None)

			if corresponding_block:
				corresponding_block.line_blocks.append(block)
			else:
				text_blocks.append(TextBlock([block]))
		else:
			text_blocks.append(TextBlock([block]))

	return text_blocks