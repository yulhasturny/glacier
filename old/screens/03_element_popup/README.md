# Screen 03: Element pop-up

![Screen 03](screen.jpg)

`screen.jpg` shows the **forest** pop-up. Further states, one per element:
- `state_rhone.jpg`: Rhone river
- `state_animals.jpg`: animals
- `state_lake-geneva.jpg`: Lake Geneva

## Description

The user has selected an element on one of the orbit rings. The view is zoomed in (zoom indicator "ZOOM ×4"). The selected element is shown **large** (a glowing circle in its color with a label and its level text below). The **ring of this element is highlighted in cyan**, the other rings are fainter. The glacier is a small cyan body at the lower right with the label "RHONEGLETSCHER". A **dashed cyan line** with the small label "DEPENDENCY" connects the element to the glacier.

At the lower left is the **pop-up**, a panel with a thin cyan border and a × button at the top right:
- **Heading:** the element name in uppercase (for example "FOREST")
- **Small heading:** "RELATIONSHIP TO THE GLACIER"
- **Text:** a short explanation of how the element depends on the glacier
- **Source line:** "SOURCE" followed by the source of the statement

The common interface elements (title, layers, RESET VIEW, timeline bar) stay visible.

Elements: Forest, Rhone river, Animals, Lake Geneva. The pop-up texts and their sources are in `data/elements.json` (one text per element). Do not write the texts into the code; load them from the file.

## Trigger

- The user clicks an element on screen 01.
- The user clicks another element while a pop-up is open.
- The user clicks ×, clicks outside the pop-up, presses Esc, or clicks RESET VIEW to close it.

## Response

- The view zooms smoothly to the selected element, with the glacier staying visible at the lower right.
- The ring of the element is highlighted, the dependency line is drawn, and the pop-up fades in without covering the element.
- Clicking another element replaces the content of the pop-up and moves the view to the new element.
- Closing the pop-up zooms back to screen 01.

## Data

- `data/elements.json`: for each element the fields `id`, `title`, `level`, `levelLabel`, `color`, `text`, `sources` (list of `{ title, url }`) and `note` (a note for the team; **do not show it** in the interface).
- The pop-up shows `title` (uppercase), `text`, and the source titles as links (small, muted) in the line "SOURCE".
- The texts in `elements.json` replace the placeholder texts mentioned above. Use the file as it is.

## Remarks

- The texts are qualitative. Do not add numbers or claims that are not backed by a source. Every text needs a `source`.
- Keep each text short (maximum about 60 words) so the pop-up stays readable.
- The wireframe places the pop-up at the lower left and the glacier at the lower right. Keep the pop-up out of the way of the selected element.
- Time slider: if the user moves the slider while a pop-up is open, the glacier body updates; the pop-up text stays.
