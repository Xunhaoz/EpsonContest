import os
from pathlib import Path

import gradio as gr
import requests

prompt_dict = {
    "Animal Classification.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste worksheet formatted for A4 printing. In the center is a large circle divided into three equal pie slices labeled “Farm Animals,” “Wild Animals,” and “Aquatic Animals” in bold, sans‑serif text; each slice contains a small cartoon animal head (a sheep, a lion, and a fish) as the gluing target. Surrounding the circle are ten full‑body animal illustrations—sheep, lamb, cow, giraffe, elephant, lion, rabbit, dolphin, turtle, and snail—each drawn with thick, uniform outlines and minimal interior detail, enclosed in a dashed “cut here” border. Playful leafy sprigs fill the spaces between, creating a balanced overhead‑view layout. Designed in a child‑friendly coloring‑book style, this worksheet invites students to color, cut out the animals, and glue them into the correct classification slice.",
    "Community Role.png": "High‑resolution, black‑and‑white line‑art coloring‑book page for a children’s cut‑and‑paste worksheet. Five friendly community helpers— a teacher holding a pointer by a chalkboard, a doctor with a stethoscope, a firefighter in uniform, a baker holding a rolling pin, and a mail carrier with a mailbag— each stands inside a dashed “cut here” rectangle with bold, sans‑serif labels beneath. In the center, a simple schematic map connects icon‑style buildings labeled SCHOOL, HOSPITAL, BAKERY, and POST OFFICE. All artwork is drawn with thick, consistent outlines and minimal detail, arranged in a balanced layout on a clean white background, ready for A4 printing.",
    "Continents Globe Puzzle.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste geography worksheet formatted for A4 printing. On the left column are six dashed‑line “cut here” silhouettes of the continents—Asia, Africa, Europe, South America, Australia, and Antarctica—each labeled in bold, sans‑serif text beneath. A vertical dashed divider splits the page. In the center is a large circle showing a simplified world map with continent outlines. To the right, a smaller globe sits inside a dashed cut‑here circle for coloring, and below it are solid‑outline blanks of the same six continent shapes—also labeled—as matching targets for gluing. All artwork uses thick, uniform strokes and minimal interior detail on a clean white background, designed in a playful, child‑friendly coloring‑book style.",
    "Food Pyramid.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste worksheet formatted for A4 printing. Dominating the page is a large food pyramid outlined in a dashed “cut here” border, divided into five labeled tiers: a small top triangle labeled “Fats & Oils,” a middle tier split into “Grains” (left) and “Fruits” (right), a full “Vegetables” layer, and a bottom tier divided into “Dairy” (left) and “Proteins” (right), all in bold, sans‑serif type. Surrounding the pyramid are individual dashed‑border cards featuring simple, thick‑lined icons: a loaf of bread, a cluster of carrots and broccoli, a leafy green, a bottle and carton, a cheese wedge, a banana, an apple, and a fish—each with its label beneath. The layout is clean and balanced on a white background, designed for children to color, cut, and paste each food into the correct pyramid section.",
    "Paper Plate Clock.png": "A high‑resolution, black‑and‑white line‑art illustration for a printable paper‑plate teaching clock. Centered is a crisp, circular clock face with bold, sans‑serif numbers 1 through 12 and fine minute tick marks, viewed straight‑on. Two simple, elongated clock hands sit to the right, ready for attachment. Surrounding the face are four friendly Australian animals drawn with thick, consistent outlines and minimal detail: a koala perched on a eucalyptus branch (top left), a kookaburra standing on a twig (top right), a kangaroo in a gentle stance (bottom left), and an echidna ambling (bottom right). Scattered leafy sprigs and gum leaves fill the negative space in a balanced, playful arrangement. Designed in a child‑friendly coloring‑book style on a clean white background, this composition combines educational clarity with a whimsical, nature‑themed motif, formatted to fit an A4 sheet.",
    "Plant.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste worksheet formatted for A4 printing. Across the top two rows are six dashed‑line square cards illustrating stages of a plant’s life cycle: “Seed” (a simple oval), “Germination” (a sprouted seed with a tiny root), “Seedling” (a small two‑leaf sprout), “Sapling” (a young multi‑leaf plant), an unlabeled mature plant silhouette, and “Fruiting” (a flowering plant). Beneath them is a long dashed‑line timeline numbered “1 2 3 4 5 6,” flanked on either side by decorative leafy sprigs. At the bottom are three dashed‑line target boxes—one labeled “Flowering,” one blank, and one labeled “Fruiting”—for students to glue the cards in sequence. All artwork is drawn with thick, consistent outlines and minimal interior detail on a clean white background, creating a playful, child‑friendly coloring and sequencing activity.",
    "Shape Puzzle Animals.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste worksheet for A4 printing. On the left: five basic shapes—circle, square, triangle, rectangle, and oval—each enclosed in a dashed “cut here” border and labeled below in bold, sans‑serif text. A vertical dashed divider runs down the center. On the right: three simple “shape puzzle” animals—CAT at the top, FISH in the middle, and BIRD at the bottom—each constructed from those shapes. Every animal part is outlined with thick, consistent lines and numbered to correspond with the shapes on the left; each number sits inside a small circle. Beneath each animal is its bold, sans‑serif name. The layout is clean, balanced, and child‑friendly, with minimal decorative detail, ready for coloring and assembly.",
    "Solar System.png": "A high‑resolution, black‑and‑white line‑art educational worksheet of the Solar System, formatted for A4 printing. On the left, a large stylized sun with crisp triangular rays; around it, nine planets (Mercury through Pluto) positioned on evenly spaced, concentric dashed orbit lines. Each planet appears as a simple circle with minimal surface details (dots for Mercury and Pluto, swirling lines for Venus and Earth, stripes for Jupiter and Uranus, rings for Saturn and Neptune), all enclosed in a dashed “cut‑here” border. Beneath each planet is a bold, sans‑serif label. The layout is an overhead, orthographic view on a clean white background, drawn with thick, consistent outlines. Designed in a playful, child‑friendly coloring‑book style that doubles as a cut‑and‑paste activity sheet.",
    "Transportation.png": "A high‑resolution, black‑and‑white line‑art activity sheet formatted for A4 printing. At the center is a large circle divided into three equal “pie” sections labeled “Land Vehicles,” “Water Vehicles,” and “Air Vehicles” in bold, sans‑serif text. Surrounding the circle are eight dashed‑line “cut here” cards, each containing a simple outline drawing—Car, Bus, Bicycle, Train, Airplane, Helicopter, Boat, and Ship—with the corresponding label beneath in the same bold font. All illustrations use thick, uniform strokes with minimal interior detail on a clean white background. Designed as a playful cut‑and‑paste sorting and coloring activity for young children.",
    "Weather and Seasons.png": "A high‑resolution, black‑and‑white line‑art cut‑and‑paste activity sheet formatted for A4 printing. At the center is a large circle divided into four equal quadrants labeled “Spring,” “Summer,” “Autumn,” and “Winter” in bold, sans‑serif text. Surrounding the circle are nine dashed‑line “cut here” cards, each containing a simple outline icon with its label below: a smiling sun (“Sunny”), a rain cloud with droplets (“Cloudy”), a classic umbrella with wind lines (“Umbrella”), a five‑petal flower (“Flower”), a stylized maple leaf (“Autumn”), and a six‑arm snowflake (“Snowflake”). All illustrations use thick, uniform strokes and minimal interior detail on a clean white background. Designed as a playful sorting, coloring, and assembly worksheet for young children.",
    "Bedroom.png": "Create a playful black‑and‑white children’s activity sheet in A4 size titled ‘COLOR THE BEDROOM!’ in bold, rounded sans‑serif letters at the top. In the upper left, draw a simple, perspective‑style bedroom interior (walls and floor) with clean, thick outlines. Surround it with eight dashed‑border cut‑out illustrations—each friendly line‑art style and labeled beneath in lowercase:\n\n- A tall wardrobe with double doors and a bottom drawer labeled ‘wardrobe’  \n- A cozy single bed with headboard labeled ‘bed’  \n- A sleek table lamp labeled ‘lamp’  \n- A two‑drawer nightstand labeled ‘nightstand’  \n- A classic alarm clock labeled ‘alarm clock’  \n- A framed picture of mountains and sun labeled ‘picture’  \n- Two small potted plants, each labeled ‘plant’\n\nEnsure each icon sits within its own dashed cut guides. Use uniform line weight and leave plenty of white space for coloring and cutting. The overall mood should be inviting and hands‑on, encouraging kids to color the scene, cut out each piece, and arrange their own cozy bedroom.",
    "Boy.png": "A bright, flat‑style educational worksheet illustrated in front‑on view: on the left, a large, smooth‑lined cartoon boy’s head silhouette with short brown hair and skin‑tone fill, centered on a clean white background. On the right, four dashed‑border cut‑out panels arranged vertically, each containing a bold, friendly line‑art facial feature—two wide round eyes, a pair of soft peach ears, a simple button nose, and a smiling mouth—each labeled in uppercase sans‑serif (“EYE,” “EAR,” “NOSE,” “MOUTH”). A pair of scissors icon marks the cut‑line. Use thick black outlines, even flat coloring, and ample white space. The overall mood is playful and inviting, reminiscent of children’s activity books, encouraging kids to color, cut, and paste their own face.",
    "Girl.png": "Create a bright, flat‑vector children’s activity sheet in A4 format with a clean white background and uniform thick black outlines.\nTitle (top center):\nIn friendly, rounded uppercase sans‑serif font:\nBuild your face! Cut and paste different body parts\nLeft side:\nA large, front‑on girl’s head silhouette with smooth, dark‑brown hair parted in the middle, simple peach‑tone skin, and plain ear outlines—no facial features—centered in its own space. Beneath it, the label FACE in bold uppercase.\nCenter:\nA vertical dashed cut‑line running down the page, punctuated by a small scissor icon in the middle.\nRight side:\nFour neatly stacked dashed‑border cut‑out panels, each containing a single flat‑color facial feature and its label in bold uppercase sans‑serif directly below:\nEYES: Two large round eyes with black pupils and white highlights.\nEARS: A matching pair of peach‑tone ears.\nNOSE: A simple, rounded button nose.\nMOUTH: A smiling mouth with red lips and white teeth.\nLeave generous white space around every element to invite coloring and cutting. The overall mood should feel playful, inviting kids to color, cut out, and create their own friendly girl’s face.",
    "Living Room.png": "Design a cheerful, black‑and‑white children’s activity worksheet in A4 format titled ‘COLOR THE LIVING ROOM!’ at the top in bold, rounded sans‑serif letters. Center a simple, perspective‑style room interior (walls and floor) with thick outlines in the upper left. Around it, arrange nine dashed‑border cut‑out icons—sofa, armchair, coffee table, shelf, clock, plant, lamp, TV, and radio—each drawn as clean, friendly line art and labeled in lowercase beneath. Maintain uniform line weight, ample white space, and clear scissor‑cut guides. The overall mood should feel playful, inviting kids to color the scene, cut out the furniture, and assemble their own cozy living room.",
    "Sandwich.png": "Create a cheerful, flat‑style children’s worksheet in A4 format with a soft cream background and bold black outlines, divided into four equal quadrants.\n\nTop‑Left Quadrant: A fully assembled triangular sandwich (two golden‑brown bread slices, a crisp green lettuce leaf, two bright red tomato slices, and a smooth yellow cheese slice) shown in vibrant color, straight‑on view.\n\nTop‑Right Quadrant: The same sandwich ingredients separated and floating in order—top bread slice, lettuce, tomato slices (side by side), cheese slice, bottom bread slice—each piece perfectly centered, with dashed borders indicating they can be cut out.\n\nBottom‑Left Quadrant: Color‑coded ingredient collage with each part stacked vertically and labeled in clear, friendly sans‑serif font: “Bread Slice,” “Lettuce,” “Tomato,” “Cheese.”\n\nBottom‑Right Quadrant: Outline‑only, black‑and‑white cut‑out templates of each ingredient (bread slice, lettuce leaf, tomato rounds, cheese diamond) arranged in the same order, with dashed edges for easy scissor cutting and blank centers for coloring.\n\nUse bright, saturated colors for the filled areas, maintain consistent line weight, and leave ample white space around each element for clarity. The overall mood should feel playful, educational, and hands‑on, inviting kids to color, cut, and assemble their own sandwich.",
}


class ColoringGalleryComponent:
    def __init__(self):
        with gr.Blocks(fill_height=True) as self.index_page:
            with gr.Row():
                for image in Path('static/cut_paste').rglob('*.png'):
                    with gr.Column():
                        gr.Image(image, height='30vh', label=image.stem)
                        with gr.Accordion("Open for Prompt!", open=False):
                            gr.Textbox(label="Prompt", lines=10, value=prompt_dict[image.name])
                            gr.Button("Copy This Idea!")
                        gr.Button("Share Your Work!")

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.index_page, path=url)
