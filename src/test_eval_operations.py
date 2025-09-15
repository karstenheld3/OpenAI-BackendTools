import os, json, math, time, re, copy
import datetime as dt

import openai
import httpx
import numpy as np

from dataclasses import dataclass
from dotenv import load_dotenv
from openai.types.shared import reasoning_effort
from openai_backendtools import *
from test_rag_operations import *

load_dotenv()

# ----------------------------------------------------- START: Evals ----------------------------------------------------------

# Item 01: FAIL - score = 0 (completely unrelated, incorrect)
# Item 02: FAIL - score = 1 (related but completely incorrect), 1 similarity ("gene expression")
# Item 03: FAIL - score = 3 (partially correct)
# Item 04: PASS - score = 5 (correct), 1 additional fact ("at least three researchers")
# Expected result: 1 of 4 questions correctly answered, 25% correct
Batch01 = [
  { "item": {
      "input": "Who is Arilena Drovik?"
      ,"reference": "Arilena Drovik is molecular biologist and geneticist. She is a Professor of Molecular Genetics and principal investigator at the Department of Molecular Biology, Lund University, Sweden. She holds a PhD in Molecular Biology from University of Cambridge, UK."
      ,"output_text": "Mahatma Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist."
      }
  }
  ,{ "item": {
    "input": "What was the title of Arilena Drovik's dissertation?"
    ,"reference": "Epigenetic Modulators of Gene Expression in Early Development"
    ,"output_text": "Epigenetic modulators, gene expression, and early development are major topics in biology."
    }
  }
  ,{ "item": {
    "input": "What was the title of Arilena Drovik's first scientific publication and where and when was it published?"
    ,"reference": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published by the 'The CRISPR Journal' in 2015."
    ,"output_text": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published in 2015."
    }
  }
  ,{ "item": {
    "input": "With whom did Arilena Drovik collaborate on scientific publications?"
    ,"reference": "Between 2018 and 2020 Arilena Drovik collaborated with the following researchers:\n- L. Fernandez and H.S. Wong on the 2018 article 'CRISPR Screening for Essential Non-Coding Elements'\n- R. Novak and other authors on the 2020 article 'Next-Generation CRISPR Tools for Precision Genome Engineering'\n"
    ,"output_text": "Arilena Drovik has collaborated with at least three researchers between 2018 and 2020:\n- on the article 'CRISPR Screening for Essential Non-Coding Elements', published in 2018, with H.S. Wong and L. Fernandez \n- on the article 'Next-Generation CRISPR Tools for Precision Genome Engineering', published in 2020, with R. Novak and other authors\n"
    }
  }
]

# Calibration batch with 60 test cases, with 10 cases for each score: 0, 1, 2, 3, 4, 5
Batch02 = [
  { "item": { "input": "Who was the first President of the United States?", "reference": "George Washington", "output_text": "Abraham Lincoln", "target_score": 0 } }
  ,{ "item": { "input": "What is the chemical symbol for gold?", "reference": "Au", "output_text": "Silver", "target_score": 0 } }
  ,{ "item": { "input": "Name the process by which plants make food using sunlight.", "reference": "Photosynthesis", "output_text": "Digestion", "target_score": 0 } }
  ,{ "item": { "input": "Capital of Spain?", "reference": "Madrid.", "output_text": "Blue.", "target_score": 0 } }
  ,{ "item": { "input": "What is H2O?", "reference": "Water.", "output_text": "", "target_score": 0 } }
  ,{ "item": { "input": "Largest mammal?", "reference": "Blue whale.", "output_text": "Elephant.", "target_score": 0 } }
  ,{ "item": { "input": "Main language of Brazil?", "reference": "Portuguese.", "output_text": "Spanish.", "target_score": 0 } }
  ,{ "item": { "input": "Currency of Japan?", "reference": "Yen.", "output_text": "Dollar.", "target_score": 0 } }
  ,{ "item": { "input": "Who painted the Mona Lisa?", "reference": "Leonardo da Vinci.", "output_text": "Picasso.", "target_score": 0 } }
  ,{ "item": { "input": "Chemical formula for salt?", "reference": "NaCl.", "output_text": "HCl.", "target_score": 0 } }

  ,{ "item": { "input": "Explain five functions of the liver in the human body.", "reference": "The liver produces bile, metabolizes nutrients, detoxifies harmful substances, stores vitamins, and regulates blood clotting.", "output_text": "The liver produces bile.", "target_score": 1 } }
  ,{ "item": { "input": "Describe five major features of the Amazon rainforest.", "reference": "The Amazon rainforest is home to diverse wildlife, spans nine countries, influences global weather, contains the world's largest river by discharge, and is threatened by deforestation.", "output_text": "The Amazon rainforest is threatened by deforestation.", "target_score": 1 } }
  ,{ "item": { "input": "Name five functions performed by the roots of a plant.", "reference": "Roots absorb water, anchor the plant, store nutrients, transport minerals, and interact with soil microbes.", "output_text": "Roots anchor the plant.", "target_score": 1 } }
  ,{ "item": { "input": "Describe five notable aspects of Paris, France.", "reference": "Paris is the capital of France, is known for the Eiffel Tower, is a center of fashion, has a rich history, and hosts the Louvre Museum.", "output_text": "Paris is a center of fashion.", "target_score": 1 } }
  ,{ "item": { "input": "Describe five features and five societal effects of inflation.", "reference": "Inflation is characterized by rising prices, decreasing currency value, higher production costs, increased wages, and reduced purchasing power. Its effects include eroded savings, uncertainty in investment, wage-price spirals, redistribution of wealth, and social unrest.", "output_text": "Inflation is characterized by rising prices, leading to eroded savings.", "target_score": 1 } }
  ,{ "item": { "input": "State five symptoms and five possible complications of untreated diabetes.", "reference": "Symptoms of untreated diabetes include excessive thirst, frequent urination, blurred vision, fatigue, and slow wound healing. Complications can be nerve damage, kidney failure, heart disease, blindness, and infections.", "output_text": "Untreated diabetes can cause excessive thirst, leading to nerve damage.", "target_score": 1 } }
  ,{ "item": { "input": "List five colors of the rainbow.", "reference": "Red, orange, yellow, green, blue, indigo, and violet are the colors of the rainbow.", "output_text": "Red is a color of the rainbow.", "target_score": 1 } }
  ,{ "item": { "input": "List five elements essential for plant growth.", "reference": "Nitrogen, phosphorus, potassium, calcium, and magnesium are essential elements for plant growth.", "output_text": "Nitrogen is essential for plant growth.", "target_score": 1 } }
  ,{ "item": { "input": "State five causes of World War I.", "reference": "The main causes of World War I were nationalism, imperialism, militarism, alliances, and the assassination of Archduke Franz Ferdinand.", "output_text": "Nationalism was a cause of World War I.", "target_score": 1 } }
  ,{ "item": { "input": "Name five human senses.", "reference": "Sight, hearing, smell, taste, and touch are the five human senses.", "output_text": "Hearing is a human sense.", "target_score": 1 } }

  ,{ "item": { "input": "List five causes and five effects of deforestation.", "reference": "Deforestation is caused by logging, agriculture, urbanization, mining, and wildfires. Its effects include loss of biodiversity, increased greenhouse gases, soil erosion, disruption of water cycles, and climate change.", "output_text": "Logging and agriculture cause deforestation, leading to increased greenhouse gases and loss of biodiversity.", "target_score": 2 } }
  ,{ "item": { "input": "List five features and five global impacts of the Himalayas.", "reference": "The Himalayas feature the world's highest peaks, vast glaciers, deep valleys, unique biodiversity, and spiritual significance. Their global impacts include regulating climate, supplying freshwater, influencing monsoons, supporting livelihoods, and attracting tourism.", "output_text": "The Himalayas have the world's highest peaks and vast glaciers, influencing monsoons and attracting tourism.", "target_score": 2 } }
  ,{ "item": { "input": "Identify five motifs and five effects found in 'Macbeth.'", "reference": "'Macbeth' features motifs of blood, darkness, supernatural elements, prophecy, and ambition. Effects include psychological torment, moral deterioration, disrupted order, guilt, and fear.", "output_text": "'Macbeth' contains the motifs of blood and ambition, leading to psychological torment and guilt.", "target_score": 2 } }
  ,{ "item": { "input": "List five principles and five challenges of democracy.", "reference": "Principles of democracy include free elections, equality before the law, separation of powers, protection of rights, and majority rule. Challenges include voter apathy, corruption, misinformation, polarization, and inequality.", "output_text": "Free elections and equality before the law are democratic principles, with challenges such as voter apathy and corruption.", "target_score": 2 } }
  ,{ "item": { "input": "List five properties and five uses of carbon.", "reference": "Carbon is nonmetallic, forms four bonds, is found in all living things, exists in several allotropes, and conducts electricity (in graphite). Uses include steel production, filters, fuels, nanotechnology, and as a reducing agent.", "output_text": "Carbon is nonmetallic and forms four bonds; it is used in steel production and as a reducing agent.", "target_score": 2 } }
  ,{ "item": { "input": "Describe five causes and five effects of World War I.", "reference": "World War I was caused by nationalism, alliances, militarism, imperialism, and the assassination of Archduke Ferdinand. Effects included the Treaty of Versailles, the League of Nations, major loss of life, redrawn borders, and political upheaval.", "output_text": "World War I was caused by militarism and alliances, leading to the Treaty of Versailles and major loss of life.", "target_score": 2 } }
  ,{ "item": { "input": "Name four major greenhouse gases and four effects of global warming.", "reference": "Major greenhouse gases include carbon dioxide, methane, nitrous oxide, and fluorinated gases. Effects of global warming are sea level rise, more extreme weather, ocean acidification, and loss of biodiversity.", "output_text": "Carbon dioxide and methane are greenhouse gases; global warming causes sea level rise and more extreme weather.", "target_score": 2 } }
  ,{ "item": { "input": "List four properties of water and their significance.", "reference": "Properties of water include high specific heat (temperature regulation), solvent ability (dissolves substances), cohesion (surface tension), and density anomaly (ice floats).", "output_text": "Water has high specific heat and acts as a solvent.", "target_score": 2 } }
  ,{ "item": { "input": "List four major contributions of Isaac Newton.", "reference": "Newton contributed the laws of motion, law of universal gravitation, calculus, and work on optics.", "output_text": "Newton is known for the laws of motion and gravity.", "target_score": 2 } }
  ,{ "item": { "input": "Name four types of economic systems and a characteristic of each.", "reference": "Economic systems include capitalism (private ownership), socialism (public ownership), mixed economy (blend), and traditional economy (custom-based).", "output_text": "Capitalism and socialism are economic systems.", "target_score": 2 } }

  ,{ "item": { "input": "List five causes and five effects of ocean pollution.", "reference": "Ocean pollution is caused by plastic waste, oil spills, agricultural runoff, untreated sewage, and chemical dumping. Effects include harm to marine life, bioaccumulation of toxins, destruction of coral reefs, reduction in fish stocks, and contamination of seafood.", "output_text": "Ocean pollution is caused by plastic waste, oil spills, and agricultural runoff, which harm marine life, cause bioaccumulation of toxins, and destroy coral reefs.", "target_score": 3 } }
  ,{ "item": { "input": "Describe five events and five outcomes of the Industrial Revolution.", "reference": "Key events included the invention of the steam engine, the rise of factories, development of railways, urbanization, and mass production. Outcomes were economic growth, social inequality, child labor, environmental pollution, and advances in technology.", "output_text": "The invention of the steam engine, rise of factories, and mass production were events of the Industrial Revolution, leading to economic growth, child labor, and advances in technology.", "target_score": 3 } }
  ,{ "item": { "input": "List five amendments and five impacts of the U.S. Constitution's Bill of Rights.", "reference": "The Bill of Rights includes the First, Second, Fourth, Fifth, and Eighth Amendments. Impacts include protection of free speech, right to bear arms, prevention of unreasonable searches, due process of law, and ban on cruel punishment.", "output_text": "The First, Second, and Fifth Amendments are included in the Bill of Rights, which protects free speech, the right to bear arms, and ensures due process of law.", "target_score": 3 } }
  ,{ "item": { "input": "List five chemical properties and five uses of oxygen.", "reference": "Oxygen is highly reactive, supports combustion, forms oxides, is colorless, and is paramagnetic. Uses include respiration, medical therapy, welding, water treatment, and rocket fuel.", "output_text": "Oxygen supports combustion, forms oxides, and is colorless. It is used in respiration, medical therapy, and welding.", "target_score": 3 } }
  ,{ "item": { "input": "Describe five features and five roles of the Amazon River.", "reference": "The Amazon River is the second longest river, has the largest drainage basin, features extensive wetlands, is home to diverse species, and has seasonal flooding. Its roles include supporting transportation, providing water, influencing climate, sustaining fisheries, and enabling trade.", "output_text": "The Amazon River is the second longest river, has the largest drainage basin, and features extensive wetlands. It supports transportation, provides water, and sustains fisheries.", "target_score": 3 } }
  ,{ "item": { "input": "Describe five goals and five achievements of the United Nations.", "reference": "The UN's goals include promoting peace, protecting human rights, fostering development, combating climate change, and providing humanitarian aid. Achievements include peacekeeping missions, Universal Declaration of Human Rights, eradication of diseases, disaster relief, and sustainable development programs.", "output_text": "The United Nations promotes peace, fosters development, and provides humanitarian aid, and has carried out peacekeeping missions, disaster relief, and sustainable development programs.", "target_score": 3 } }
  ,{ "item": { "input": "State five major inventions and five impacts of the 20th century.", "reference": "Major inventions: airplane, computer, television, antibiotic drugs, and nuclear power. Impacts: increased global communication, longer life expectancy, rapid information exchange, new warfare, and energy transformation.", "output_text": "The airplane and the computer were major 20th-century inventions, leading to increased global communication, longer life expectancy, rapid information exchange, new warfare, and energy transformation.", "target_score": 3 } }
  ,{ "item": { "input": "List five forms of renewable energy and five challenges associated with their adoption.", "reference": "Forms: solar, wind, hydro, geothermal, tidal. Challenges: cost, intermittency, storage, land use, and grid integration.", "output_text": "Solar, wind, hydro, and geothermal are renewable energy forms, facing challenges like cost and intermittency.", "target_score": 3 } }
  ,{ "item": { "input": "Describe five major battles and five outcomes of World War II.", "reference": "Battles: Stalingrad, Midway, Normandy, El Alamein, Bulge. Outcomes: Allied victory, end of the Holocaust, UN formation, Europe's division, start of Cold War.", "output_text": "Stalingrad, Midway, and Normandy were major battles of World War II, which resulted in Allied victorly, end of the Holocaust, UN formation, Europe's division, and start of the Cold War.", "target_score": 3 } }
  ,{ "item": { "input": "List five composers and five genres they influenced.", "reference": "Composers: Bach, Mozart, Beethoven, Tchaikovsky, Stravinsky. Genres: Baroque, Classical, Romantic, Ballet, Modern.", "output_text": "Bach and Mozart were influential composers in Baroque and Classical music, along with Beethoven, who influenced Romantic, Ballet, and Modern genres.", "target_score": 3 } }

  ,{ "item": { "input": "List five features and five benefits of a market economy.", "reference": "Features: competition, private property, voluntary exchange, consumer choice, limited government intervention. Benefits: efficiency, innovation, variety, lower prices, higher quality.", "output_text": "A market economy features competition, private property, voluntary exchange, and consumer choice. It results in efficiency, innovation, variety, and lower prices.", "target_score": 4} }
  ,{ "item": { "input": "Describe five features and five global impacts of the Sahara Desert.", "reference": "Features: world's largest hot desert, vast sand dunes, extreme temperatures, scarce water, unique flora and fauna. Impacts: climate influence, migration patterns, trade routes, mineral resources, tourism.", "output_text": "The Sahara is the world's largest hot desert, with vast sand dunes, extreme temperatures, and scarce water. Its impacts include climate influence, migration patterns, trade routes, and mineral resources.", "target_score": 4} }
  ,{ "item": { "input": "List five symptoms and five possible complications of untreated diabetes.", "reference": "Symptoms: excessive thirst, frequent urination, fatigue, blurred vision, slow wound healing. Complications: nerve damage, kidney failure, heart disease, blindness, infections.", "output_text": "Untreated diabetes can cause excessive thirst, frequent urination, fatigue, and blurred vision, and may lead to nerve damage, kidney failure, heart disease, and blindness.", "target_score": 4} }
  ,{ "item": { "input": "Describe five features and five advantages of electric cars.", "reference": "Features: battery-powered, regenerative braking, silent operation, instant torque, remote monitoring. Advantages: zero emissions, lower operating cost, quiet ride, fast acceleration, reduced maintenance.", "output_text": "Electric cars have battery power, regenerative braking, silent operation, and instant torque. They offer zero emissions, lower operating cost, quiet ride, and fast acceleration.", "target_score": 4} }
  ,{ "item": { "input": "List five ancient civilizations and five of their achievements.", "reference": "Civilizations: Sumer, Egypt, Indus Valley, China, Mesoamerica. Achievements: writing, monumental architecture, irrigation, mathematics, astronomy.", "output_text": "Sumer, Egypt, Indus Valley, and China were ancient civilizations. Their achievements included writing, monumental architecture, irrigation, and mathematics.", "target_score": 4} }
  ,{ "item": { "input": "List five endangered species and five conservation efforts to protect them.", "reference": "Endangered species: Amur leopard, Sumatran orangutan, Javan rhino, Hawksbill turtle, Vaquita. Efforts: habitat protection, anti-poaching laws, captive breeding, pollution control, international agreements.", "output_text": "The Amur leopard, Sumatran orangutan, Javan rhino, and Hawksbill turtle are endangered species. Conservation efforts include habitat protection, anti-poaching laws, captive breeding, pollution control, and international agreements.", "target_score": 4} }
  ,{ "item": { "input": "List five major world religions and four of their core beliefs.", "reference": "Religions: Christianity, Islam, Hinduism, Buddhism, Judaism. Core beliefs: monotheism, afterlife, compassion, ritual, reincarnation.", "output_text": "Christianity, Islam, Hinduism, Buddhism, and Judaism are major world religions. They share beliefs in monotheism, afterlife, compassion, and ritual.", "target_score": 4} }
  ,{ "item": { "input": "List five world capitals and describe three of their cultural contributions.", "reference": "Capitals: London, Paris, Tokyo, Cairo, Sydney. Contributions: art, fashion, cuisine, literature, festivals.", "output_text": "London, Paris, Tokyo, Cairo, and Sydney are world capitals, famous for art, fashion, and cuisine.", "target_score": 4} }
  ,{ "item": { "input": "Describe five major U.S. Supreme Court cases and four of their legal precedents.", "reference": "Cases: Marbury v. Madison, Brown v. Board, Roe v. Wade, Miranda v. Arizona, Obergefell v. Hodges. Precedents: judicial review, desegregation, abortion rights, self-incrimination, marriage equality.", "output_text": "Marbury v. Madison, Brown v. Board, Roe v. Wade, and Miranda v. Arizona are major cases that established judicial review, desegregation, abortion rights, and self-incrimination rights.", "target_score": 4} }
  ,{ "item": { "input": "Identify five symbols and five meanings in 'The Lord of the Flies.'", "reference": "Symbols: conch shell, Piggys glasses, the fire, the beast, the Lord of the Flies. Meanings: order, knowledge, hope, fear, savagery.", "output_text": "The conch shell, Piggy's glasses, the fire, and the beast are symbols in 'The Lord of the Flies.' They represent order, knowledge, hope, and fear.", "target_score": 4} }

  ,{ "item": { "input": "List five components and five functions of the human circulatory system.", "reference": "The circulatory system includes the heart, arteries, veins, capillaries, and blood. Its functions are transporting oxygen, removing waste, delivering nutrients, regulating temperature, and supporting immune response.", "output_text": "Key components of the circulatory system are blood, capillaries, arteries, heart, and veins. Its main functions include delivering nutrients, regulating body temperature, supporting immune response, transporting oxygen, and removing waste.", "target_score": 5 } }
  ,{ "item": { "input": "List five symptoms and five possible complications of untreated diabetes.", "reference": "Symptoms of untreated diabetes include excessive thirst, frequent urination, fatigue, blurred vision, and slow wound healing. Complications can be nerve damage, kidney failure, heart disease, blindness, and infections.", "output_text": "Untreated diabetes symptoms include blurred vision, excessive thirst, fatigue, slow wound healing, and frequent urination. Possible complications are infections, blindness, heart disease, nerve damage, and kidney failure.", "target_score": 5 } }
  ,{ "item": { "input": "Identify five Impressionist painters and five hallmarks of the movement.", "reference": "Impressionist painters include Monet, Renoir, Degas, Pissarro, and Sisley. Hallmarks of Impressionism are loose brushwork, vibrant color, focus on light, open composition, and modern life subjects.", "output_text": "Among Impressionist painters are Pissarro, Monet, Degas, Renoir, and Sisley. Impressionism is noted for vibrant color, open composition, loose brushwork, a focus on light, and modern life subjects.", "target_score": 5 } }
  ,{ "item": { "input": "List five Nobel Prize categories and five notable recipients for each.", "reference": "Categories: Peace, Literature, Physics, Chemistry, Medicine. Notable recipients: Mother Teresa, Ernest Hemingway, Albert Einstein, Marie Curie, Alexander Fleming.", "output_text": "Nobel Prize categories are Medicine, Chemistry, Peace, Literature, and Physics. Notable winners include Ernest Hemingway, Albert Einstein, Mother Teresa, Marie Curie, and Alexander Fleming.", "target_score": 5 } }
  ,{ "item": { "input": "List five branches of biology and five research focuses for each.", "reference": "Branches: zoology, botany, microbiology, genetics, ecology. Focuses: animal life, plant life, microorganisms, heredity, ecosystems.", "output_text": "Five branches of biology are genetics, botany, zoology, ecology, and microbiology. Their focuses are animal life, plant life, heredity, ecosystems, and microorganisms.", "target_score": 5 } }
  ,{ "item": { "input": "List five fundamental forces of nature and their five main effects.", "reference": "Forces: gravity, electromagnetism, strong nuclear, weak nuclear, friction. Effects: planetary orbits, electricity, atomic stability, radioactive decay, resistance to motion.", "output_text": "The five fundamental forces are strong nuclear, gravity, weak nuclear, friction, and electromagnetism. Their main effects include electricity, resistance to motion, atomic stability, planetary orbits, and radioactive decay.", "target_score": 5 } }
  ,{ "item": { "input": "List five elements of the periodic table and five ways each is used in industry.", "reference": "Elements: hydrogen, oxygen, carbon, iron, copper. Uses: fuel, water treatment, steel, construction, electrical wiring.", "output_text": "Oxygen, hydrogen, carbon, iron, and copper are elements of the periodic table. They are used in water treatment, fuel, steel, construction, and electrical wiring.", "target_score": 5 } }
  ,{ "item": { "input": "List five continents and five distinctive geographic features of each.", "reference": "Continents: Africa, Asia, Europe, North America, South America. Features: Sahara Desert, Himalayas, Alps, Rocky Mountains, Amazon River.", "output_text": "Asia, Africa, North America, South America, and Europe are continents. Their features include the Himalayas, Sahara Desert, Rocky Mountains, Amazon River, and Alps.", "target_score": 5 } }
  ,{ "item": { "input": "Name five Shakespearean tragedies and five central themes present in each.", "reference": "Tragedies: Hamlet, Macbeth, Othello, King Lear, Romeo and Juliet. Themes: ambition, betrayal, fate, madness, love.", "output_text": "Central Shakespearean tragedies include Macbeth, King Lear, Romeo and Juliet, Hamlet, and Othello. Common themes are ambition, love, madness, betrayal, and fate.", "target_score": 5 } }
  ,{ "item": { "input": "List five major mountain ranges and five countries in which they are found.", "reference": "Ranges: Andes, Alps, Himalayas, Rockies, Appalachians. Countries: Chile, Switzerland, Nepal, United States, Canada.", "output_text": "Major mountain ranges are the Rockies, Andes, Himalayas, Alps, and Appalachians. Countries where these are found include United States, Nepal, Canada, Chile, and Switzerland.", "target_score": 5 } }
]

# ----------------------------------------------------- END: Evals ------------------------------------------------------------

# ----------------------------------------------------- START: Prompts --------------------------------------------------------
# A very simple judge model prompt
judge_model_prompt_template_1 = """
You are an expert evaluator for a QA system.
Compare the generated model output ('model_output' tag) to the reference answer ('reference' tag).
If you have the question ('input' tag), also consider the input when comparing the model output to the reference answer.
Assign an **integer score from 0 to 5** where:
- Score 0 = completely unrelated and incorrect
- Score 1 = related but completely incorrect
- Score 2 = mostly incorrect
- Score 3 = partially correct
- Score 4 = mostly correct
- Score 5 = completely correct

Also explain your reasoning. Return exactly:
```json
{
  "score": <0-5>,
  "rationale": [ "<reasoning>" ]
}
```

<input>
{{ item.input }}
</input>

<reference>
{{ item.reference }}
</reference>

<model_output>
{{ item.output_text }}
</model_output>
"""

# A detailed judge model prompt using multiple criteria
judge_model_prompt_template_2 = """
## Task

You are an evaluator. Compare a GPT model's output (`output_text`) against a reference answer (`reference`) and assign an **integer score from 0 to 5**. Also provide a brief bullet-point rationale tying each point in your score back to the criteria below.

### 1. Criteria to check

For each evaluation, first list each fact, conclusion, and key term from the reference.
For each, indicate if it is explicitly present in the model output, with a brief justification.
Then calculate ratios as required.

#### Definitions

- **Facts**: A fact is a verifiable, objective statement that describes reality without inference, opinion, or interpretation. See examples below.  
- **Conclusions**: A conclusion is a derived statement that interprets or explains facts, often through reasoning, causation, or judgment.
  - If removing the sentence would make the text lose an interpretation, not a data point—it's likely a conclusion.
- **Example**:
  - Fact 1: Revenue grew by 25% in Q2.
  - Fact 2: Marketing expenses were reduced by 15% over the same period.
  - Fact 3: Customer acquisition rose by 18%.
  - Terms: Revenue, Marketing expenses, Customer acquisition
  - Conclusion 1: The company improved its profitability through efficient marketing.
  - Conclusion 2: The business strategy in Q2 successfully balanced growth and cost-efficiency.

#### Scoring

- **Facts (40%)**  
  - Identify each discrete fact in the reference.
  - Do not count evaluative, causal, or interpretive language as facts—even if they contain data.
  - Check whether the same fact appears correctly in the model output.
  - Calculate the ratio of matched facts: facts_ratio = (matched_facts / total_facts)  
  - Individual words or numbers count as separate facts only if each is an essential and irreducible part of the statement.
  - Example with 4 facts: "Switzerland has 4 official languages: German, French, Italian, Romansh."
  - Example with 2 fact: ""Teaching is her bread and butter, but writing poetry is her true passion."
- **Conclusions (30%)**  
  - Identify key conclusions or judgments.
  - Do not re-count previously identified facts as conclusions. Only count statements that derive or infer meaning from facts.
  - Check whether the model output reaches the same conclusions.
  - Calculate the ratio of matched conclusions: conclusions_ratio = (matched_conclusions / total_conclusions)
  - All conclusions have to be explicitly stated in the model output. Implicit conclusions do not count as matched.
- **Terminology (21%)**  
  - List each key term in the reference without counting values and numeric expressions ('10 orders', '20%', 'less than 5') as terms.
  - Check whether the model output uses the same terms.
  - Calculate the ratio of matched terms: terms_ratio = (matched_terms / total_terms)
    - If total_terms > 0, then terms_ratio = (matched_terms / total_terms)
    - If total_terms == 0, set terms_ratio = 1
    - If no terms are matched, terms_ratio = 0
- **Organization (9%)**
  - Compare the high-level structure (sections, ordering) of the model output and reference.
  - Calculate the ratio of matched organization (0 or 1): organization_ratio = 0 for very different, 1 for comparable

### 2. Scoring model

- **If total_conclusions > 0:**
  - score = 5 * ( (facts_ratio * 0.4) + (conclusions_ratio * 0.3) + (terms_ratio * 0.21) + (organization_ratio * 0.09) )
- **If total_conclusions == 0:**
  - score = 5 * ( (facts_ratio * 0.7) + (terms_ratio * 0.21) + (organization_ratio * 0.09) )
- **If matched_facts < 1:**
  - score = 5 * ( (facts_ratio * 0.7) + (terms_ratio * 0.21) )
- IMPORTANT: Round the score to the nearest integer number

### 3. Score verification

Verify that the score calculation is correct by breaking it down to smaller steps.

### 4. Output format

Return exactly:

```json
{
  "score": <0-5>,
  "rationale": [
    "Fact: <number_of_output_facts> of <number_of_reference_facts> correctly matched.",
    "Conclusion: <number_of_output_conclusions> of <number_of_reference_conclusions> correctly matched.",
    "Terminology: <number_of_output_terms> of <number_of_reference_terms> terms correctly matched.",
    "Organization: matched/mismatched",
    "Score: <score_rounded> ≈ <score_exact> = <score_calculation>"
  ]
}
```

### 5. Examples

- **Reference:** There are 27 member states in the European Union, and 8 of them use their own national currencies instead of the Euro.
- 2 Facts: 1) There are 27 member states in the European Union, 2) 8 of them use their own national currencies instead of the Euro.
- 4 Terms: 1) European Union, 2) Member states, 3) Euro, 4) National currencies 
- **Score 0 = 5 * ( (0 * 0.7) + (0 * 0.2) + (0 * 0.1) ):** Bla bla.
- **Score 1 = 5 * ( (0 * 0.7) + (1 * 0.2) + (0 * 0.1) ):** The Euro is the currency of the European Union. But some member states use their own national currencies.
- **Score 2 = 5 * ( (0.5 * 0.7) + (0.25 * 0.2) + (0 * 0.1) ):** There are 27 member states.
- **Score 3 = 5 * ( (0.5 * 0.7) + (1 * 0.2) + (1 * 0.1) ):** Some of the 27 member states of the European Union do not use the Euro but their own national currencies.
- **Score 4 = 5 * ( (1 * 0.7) + (0.5 * 0.2) + (0 * 0.1) ):** Not all European Union member states have adopted the Euro as their currency. Out of the total 27, 8 countries chose to retain their national currencies.
- **Score 5 = 5 * ( (1 * 0.7) + (1 * 0.2) + (1 * 0.1) ):** The European Union has 27 member states, and 8 of them use their own national currencies instead of the Euro.

### 6. Data

<input>
{{ item.input }}
</input>

<reference>
{{ item.reference }}
</reference>

<model_output>
{{ item.output_text }}
</model_output>
"""

# This is the langchain open evals correctness prompt
# https://github.com/langchain-ai/openevals/blob/main/python/openevals/prompts/correctness.py
judge_model_prompt_template_3 = """
You are an expert data labeler evaluating model outputs for correctness. Your task is to assign a score based on the following rubric:

<Rubric>
  A correct answer:
  - Provides accurate and complete information
  - Contains no factual errors
  - Addresses all parts of the question
  - Is logically consistent
  - Uses precise and accurate terminology

  When scoring, you should penalize:
  - Factual errors or inaccuracies
  - Incomplete or partial answers
  - Misleading or ambiguous statements
  - Incorrect terminology
  - Logical inconsistencies
  - Missing key information
</Rubric>

<Instructions>
  - Carefully read the input and output
  - Check for factual accuracy and completeness
  - Focus on correctness of information rather than style or verbosity
</Instructions>

<Reminder>
  The goal is to evaluate factual correctness and completeness of the response.
</Reminder>

<input>
{{ item.input }}
</input>

<model_output>
{{ item.output_text }}
</model_output>

Use the reference outputs below to help you evaluate the correctness of the response:

<reference_outputs>
{{ item.reference }}
</reference_outputs>
"""

# Azure AI Foundry "Model Scorer > Semantic Similarity" prompt (2025-08-13). Modified to also return return score 0-5 (instead of 1-5)
judge_model_prompt_template_4 = """
Evaluate the degree of similarity between the given output and the ground truth on a scale from 0 to 5, using a chain of thought to ensure step-by-step reasoning before reaching the conclusion.

Consider the following criteria:

- 5: Highly similar - The output and ground truth are nearly identical, with only minor, insignificant differences.
- 4: Somewhat similar - The output is largely similar to the ground truth but has few noticeable differences.
- 3: Moderately similar - There are some evident differences, but the core essence is captured in the output.
- 2: Slightly similar - The output only captures a few elements of the ground truth and contains several differences.
- 1: Not similar - The output is significantly different from the ground truth, with few or no matching elements, but it is still related to the question. 
- 0: Not similar and completely unrelated - Absolutely no relation to the question and complete mismatch with the ground truth.

# Steps

1. Identify and list the key elements present in both the output and the ground truth.
2. Compare these key elements to evaluate their similarities and differences, considering both content and structure.
3. Analyze the semantic meaning conveyed by both the output and the ground truth, noting any significant deviations.
4. Based on these comparisons, categorize the level of similarity according to the defined criteria above.
5. Write out the reasoning for why a particular score is chosen, to ensure transparency and correctness.
6. Assign a similarity score based on the defined criteria above.

# Output Format

Provide the final similarity score as an integer (0, 1, 2, 3, 4, or 5).

# Examples

**Example 1:**

- Output: "The cat sat on the mat."
- Ground Truth: "The feline is sitting on the rug."
- Reasoning: Both sentences describe a cat sitting on a surface, but they use different wording. The structure is slightly different, but the core meaning is preserved. There are noticeable differences, but the overall meaning is conveyed well.
- Similarity Score: 3

**Example 2:**

- Output: "The quick brown fox jumps over the lazy dog."
- Ground Truth: "A fast brown animal leaps over a sleeping canine."
- Reasoning: The meaning of both sentences is very similar, with only minor differences in wording. The structure and intent are well preserved.
- Similarity Score: 4

# Notes

- Always aim to provide a fair and balanced assessment.
- Consider both syntactic and semantic differences in your evaluation.
- Consistency in scoring similar pairs is crucial for accurate measurement.

# Data

<output>
{{ item.output_text }}
</output>

<ground_truth>
{{ item.reference }}
</ground_truth>

<question>
{{ item.input }}
</question>
"""
# Azure AI Foundry "Likert-Scale Evaluator > Similarity" prompt (2025-08-13). Modified to also return return score 0-5 (instead of 1-5)
judge_model_prompt_template_5 = """
system:
You are an AI assistant. You will be given the definition of an evaluation metric for assessing the quality of an answer in a question-answering task.
Your job is to compute an accurate evaluation score using the provided evaluation metric.s
You should return a single integer value between 0 to 5 representing the evaluation metric. You will include no other text or information.
user:
Equivalence, as a metric, measures the similarity between the predicted answer and the correct answer.
If the information and content in the predicted answer is similar or equivalent to the correct answer, then the value of the Equivalence metric should be high, else it should be low.
Given the question, correct answer, and predicted answer, determine the value of Equivalence metric using the following rating scale:

Score 0: the predicted answer is not at all similar to the correct answer and completely unrelated to the question
Score 1: the predicted answer is not at all similar to the correct answer but at somewhat related to the question
Score 2: the predicted answer is mostly not similar to the correct answer
Score 3: the predicted answer is somewhat similar to the correct answer
Score 4: the predicted answer is mostly similar to the correct answer
Score 5: the predicted answer is completely similar to the correct answer

This rating value should always be an integer between 0 and 5. So the rating produced should be 0 or 1 or 2 or 3 or 4 or 5.

The examples below show the Equivalence score for a question, a correct answer, and a predicted answer.

question: Who was the first president of the USA?
correct answer: George Washington
predicted answer: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
score: 0

question: What is the role of ribosomes?
correct answer: Ribosomes are cellular structures responsible for protein synthesis. They interpret the genetic information carried by messenger RNA (mRNA) and use it to assemble amino acids into proteins.
predicted answer: Ribosomes participate in carbohydrate breakdown by removing nutrients from complex sugar molecules.
score: 1

question: Why did the Titanic sink?
correct answer: The Titanic sank after it struck an iceberg during its maiden voyage in 1912. The impact caused the ship's hull to breach, allowing water to flood into the vessel. The ship's design, lifeboat shortage, and lack of timely rescue efforts contributed to the tragic loss of life.
predicted answer: The sinking of the Titanic was a result of a large iceberg collision. This caused the ship to take on water and eventually sink, leading to the death of many passengers due to a shortage of lifeboats and insufficient rescue attempts.
score: 2

question: What causes seasons on Earth?
correct answer: Seasons on Earth are caused by the tilt of the Earth's axis and its revolution around the Sun. As the Earth orbits the Sun, the tilt causes different parts of the planet to receive varying amounts of sunlight, resulting in changes in temperature and weather patterns.
predicted answer: Seasons occur because of the Earth's rotation and its elliptical orbit around the Sun. The tilt of the Earth's axis causes regions to be subjected to different sunlight intensities, which leads to temperature fluctuations and alternating weather conditions.
score: 3

question: How does photosynthesis work?
correct answer: Photosynthesis is a process by which green plants and some other organisms convert light energy into chemical energy. This occurs as light is absorbed by chlorophyll molecules, and then carbon dioxide and water are converted into glucose and oxygen through a series of reactions.
predicted answer: In photosynthesis, sunlight is transformed into nutrients by plants and certain microorganisms. Light is captured by chlorophyll molecules, followed by the conversion of carbon dioxide and water into sugar and oxygen through multiple reactions.
score: 4

question: What are the health benefits of regular exercise?
correct answer: Regular exercise can help maintain a healthy weight, increase muscle and bone strength, and reduce the risk of chronic diseases. It also promotes mental well-being by reducing stress and improving overall mood.
predicted answer: Routine physical activity can contribute to maintaining ideal body weight, enhancing muscle and bone strength, and preventing chronic illnesses. In addition, it supports mental health by alleviating stress and augmenting general mood.
score: 5

<question>
{{ item.input }}
</question>

<correct_answer>
{{ item.reference }}
</correct_answer>

<predicted_answer>
{{ item.output_text }}
</predicted_answer>
"""

# https://github.com/run-llama/llama_index/blob/5e904433c9aa1de63d8a01dd117e19e8ed336ede/llama-index-core/llama_index/core/evaluation/correctness.py#L19
# LlamaIndex CorrectnessEvaluator prompt, asking for a 1–5 rating
judge_model_prompt_template_6 = """
You are an expert evaluation system for a question answering chatbot.

You are given the following information:
- a user query, and
- a generated answer

You may also be given a reference answer to use for reference in your evaluation.

Your job is to judge the relevance and correctness of the generated answer.
Output a single score that represents a holistic evaluation.
You must return your response in a line with only the score.
Do not return answers in any other format.
On a separate line provide your reasoning for the score as well.

Follow these guidelines for scoring:
- Your score has to be between 1 and 5, where 1 is the worst and 5 is the best.
- If the generated answer is not relevant to the user query, you should give a score of 1.
- If the generated answer is relevant but contains mistakes, you should give a score between 2 and 3.
- If the generated answer is relevant and fully correct, you should give a score between 4 and 5.

Example Response:
4.0
The generated answer has the exact same metrics as the reference answer, \
    but it is not as concise.
"""

# ----------------------------------------------------- END: Prompts ----------------------------------------------------------

# ----------------------------------------------------- START: Tests ----------------------------------------------------------

# Gets all answers for the 'input' in all items using responses API with enhanced parameters and stores them in 'output_text' of each items
def get_answers_from_model_and_return_items(client, vector_store_id, model, items, instructions=None, temperature=0, reasoning_effort=None):
  function_name = 'Get answers from model using responses API and add to items'
  start_time = log_function_header(function_name)
  
  # Make a deep copy of items to avoid modifying the original
  items_copy = copy.deepcopy(items)

  for idx, item in enumerate(items_copy, 1):
    input = item['item']['input']
    print(f"  [ {idx} / {len(items)} ] Query: {input}")
    
    # Build request parameters for responses API
    request_params = {
      "model": model,
      "input": input,
      "tools": [{ "type": "file_search", "vector_store_ids": [vector_store_id] }],
      "temperature": temperature
    }
    
    # Add instructions if provided
    if instructions: request_params["instructions"] = instructions
    
    # Remove temperature parameter for reasoning models that don't support it
    # This function also handles adding reasoning configuration (effort)
    remove_temperature_from_request_params_for_reasoning_models(request_params, model, reasoning_effort)
    
    response = retry_on_openai_errors(lambda: client.responses.create(**request_params), indentation=4)
    output_text = response.output_text
    print(f"    Response: {truncate_string(remove_linebreaks(output_text),80)}")
    item['item']['output_text'] = output_text

  log_function_footer(function_name, start_time)
  return items_copy, "OK"

# Embedds (vectorizes) reference and model output, then gets scores for all items using cosine similarity and adds score and rationale to each item
def score_answers_using_cosine_similarity_and_return_items(client, items, embedding_model="text-embedding-3-small", log_details: bool = True):
  function_name = 'Evaluate answers using cosine similarity'
  start_time = log_function_header(function_name)
  
  # Make a deep copy of items to avoid modifying the original
  items_copy = copy.deepcopy(items)

  def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

  def embed_text(text):
    response = retry_on_openai_errors(lambda: client.embeddings.create(
      model=embedding_model,
      input=[text]
    ), indentation=4)
    return response.data[0].embedding

  for idx, item in enumerate(items_copy, 1):
    input = item['item']['input']
    reference = item['item']['reference']
    output_text = item['item'].get('output_text', '')
    print(f"  [ {idx} / {len(items)} ] Query: {truncate_string(input.replace('\n', ' '),120)}")
    if log_details:
      print(f"    Reference    : {truncate_string(reference.replace('\n', ' '),100)}")
      print(f"    Model output : {truncate_string(remove_linebreaks(output_text),100)}")

    try:
      # Get embeddings and calculate similarity
      reference_embedding = embed_text(reference)
      output_embedding = embed_text(output_text)
      similarity = cosine_similarity(reference_embedding, output_embedding)
      
      # Convert similarity score (0-1) to evaluation score (1-5)
      score = int(round(similarity * 4)) + 1
      
      # Add score and rationale to the item
      item['item']['score'] = score
      item['item']['rationale'] = [f"Cosine similarity: {similarity:.3f} (mapped to score {score})"] 
      
      if log_details:
        print(f"    Score: {score}")
        print(f"    - Similarity: {similarity:.3f}")
    except Exception as e:
      print(f"    Error: Could not calculate embedding similarity: {str(e)}")
      item['item']['score'] = 0
      item['item']['rationale'] = [f"Error calculating similarity score: {str(e)}"]

  log_function_footer(function_name, start_time)
  return items_copy, "OK"

# Gets scores for all items using the provided prompt template and add score and rationale to each item
def score_answers_using_judge_model_and_return_items(client, items, prompt_template, judge_model_name, remove_input_from_prompt: bool = False, log_details: bool = True):
  function_name = 'Evaluate answers and add scores in items'
  start_time = log_function_header(function_name)
  
  # Make a deep copy of items to avoid modifying the original
  items_copy = copy.deepcopy(items)

  for idx, item in enumerate(items_copy, 1):
    input = item['item']['input']
    reference = item['item']['reference']
    output_text = item['item'].get('output_text', '')
    print(f"  [ {idx} / {len(items)} ] Query: {truncate_string(input.replace('\n', ' '),120)}")
    if log_details:
      print(f"    Reference    : {truncate_string(reference.replace('\n', ' '),100)}")
      print(f"    Model output : {truncate_string(remove_linebreaks(output_text),100)}")
   
    # Replace placeholders in the prompt template
    prompt = re.sub(r'{{\s*item.reference\s*}}', reference, prompt_template)
    prompt = re.sub(r'{{\s*item.output_text\s*}}', output_text, prompt)
    if remove_input_from_prompt:
      # remove tags <input></input> and everything in between
      prompt = re.sub(r'<input>.*?</input>', '', prompt)
    else:
      prompt = re.sub(r'{{\s*item.input\s*}}', input, prompt)
    
    # Call the OpenAI API to evaluate the answer
    request_params = {
      "model": judge_model_name,
      "input": prompt,
      "text": { "format": { "type": "json_object" } },
      "temperature": 0
    }
    
    # Remove temperature parameter for reasoning models that don't support it
    remove_temperature_from_request_params_for_reasoning_models(request_params, judge_model_name)
    
    response = retry_on_openai_errors(lambda: client.responses.create(**request_params), indentation=4)
    
    # Parse the JSON response
    try:
      evaluation = json.loads(response.output_text)
      score = evaluation.get('score')
      rationale = evaluation.get('rationale')
      
      # Add score and rationale to the item
      item['item']['score'] = score
      item['item']['rationale'] = rationale
      
      if log_details:
        print(f"    Score: {score}")
        for r in rationale:
          print(f"    - {truncate_string(r,120) }")
    
    except json.JSONDecodeError:
      print(f"    Error: Could not parse JSON response: {response.output_text}")
      item['item']['score'] = None
      item['item']['rationale'] = ["Error: Could not parse evaluation"]

  log_function_footer(function_name, start_time)
  return items_copy, "OK"

def score_answers_using_score_model_grader_and_return_items(client, items, eval_name, prompt_template, eval_model, min_score: int, remove_input_from_prompt: bool, delete_eval_after_run: bool = False, log_details: bool = True):
  function_name = 'Evaluate answers using score model grader'
  start_time = log_function_header(function_name)
  
  # Make a deep copy of items to avoid modifying the original
  items_copy = copy.deepcopy(items)
  
  # Add index property to all items if not already existing
  for idx, item in enumerate(items_copy):
    if 'index' not in item['item']:
      item['item']['index'] = idx

  # Reset 'score' and 'rationale' for each item
  for item in items_copy: item['item']['score'] = -1; item['item']['rationale'] = ""

  if remove_input_from_prompt:
    # remove tags <input></input> and everything in between
    prompt_template = re.sub(r'<input>.*?</input>', '', prompt_template)

  testing_criteria_item={
    "type": "score_model", "name": "Answer Quality Score", "model": eval_model
    ,"sampling_params": { "temperature": 0 }
    ,"input": [ {"role": "system", "content": prompt_template } ]
    ,"range": [0, 5], "pass_threshold": min_score
  }

  # if eval model name starts with 'o', remove sampling_params attribute because o-models do not support temperature -> results will be empty
  if eval_model.startswith('o') or eval_model.startswith('gpt-5'): del testing_criteria_item['sampling_params']

  # Does not work as of 2025-08-17 (reasoning_effort is not supported).
  # remove_temperature_from_request_params_for_reasoning_models(testing_criteria_item["sampling_params"], eval_model,"high")

  # Create evaluation configuration with custom graders
  # https://platform.openai.com/docs/api-reference/graders/score-model
  eval_cfg = client.evals.create(
    name=eval_name,
    data_source_config={
      "type": "custom"
      ,"item_schema": {
        "type": "object"
        ,"properties": { "input": {"type": "string"}, "reference": {"type": "string"}, "output_text": {"type": "string"} }
        ,"required": ["input", "reference", "output_text"]
      },
      "include_sample_schema": False
    },
    testing_criteria=[testing_criteria_item]
  )

  # Create and run evaluation
  eval_run = client.evals.runs.create(
    name=eval_name.lower().replace(" ", "_") + "_run",
    eval_id=eval_cfg.id,
    data_source={
      "type": "jsonl", "source": { "type": "file_content", "content": items_copy }
    }
  )
  print(f"  Created evaluation run with ID: {eval_run.id}")
  print(f"  View results at: {eval_run.report_url}")

  # Poll for completion
  attempts = 0; sleep_time_in_seconds = 10; max_attempts = math.ceil((10 * len(items)) / sleep_time_in_seconds) + 5 # 10 seconds per item + 5 additional retries
  while attempts < max_attempts:
    try:
      status = client.evals.runs.retrieve(eval_run.id, eval_id=eval_cfg.id).status
    except (openai.APITimeoutError, httpx.ConnectTimeout) as e:
      print(f"  Eval completion polling timeout occurred...")
    if status == "completed": print("  Evaluation completed."); break
    elif status == "failed": print("  ERROR: Evaluation failed.");
    else:
      attempts += 1
      print(f"  [ {attempts} / {max_attempts} ] Waiting {sleep_time_in_seconds} seconds for completion...")
      time.sleep(sleep_time_in_seconds)
  
  if attempts >= max_attempts:
    raise TimeoutError(f"Evaluation timed out after {max_attempts} attempts")

  # Get results and update items
  # results = client.evals.runs.retrieve(eval_run.id, eval_id=eval_cfg.id)
  # total_count, passed_count, failed_count, errored_count = results.result_counts.total, results.result_counts.passed, results.result_counts.failed, results.result_counts.errored
  
  # Get all output items with pagination handling
  output_items = get_all_eval_run_output_items(client, run_id=eval_run.id, eval_id=eval_cfg.id, expected_count=len(items_copy), max_retries=5)

  # Run over all items and update their score and rationale from the evaluation results
  for idx, item in enumerate(items_copy):
    if log_details: print(f"  [ {idx + 1} / {len(items)} ] Query: {truncate_string(item['item']['input'].replace('\n', ' '),120)}")
    # Find matching output item for this input item - try index first, then fallback to input/reference matching
    output_item = None
    item_index = item['item'].get('index', idx)  # Use stored index or calculate from enumerate
    
    # Try matching by index first
    try:
      output_item = next(o for o in output_items if 'index' in o.datasource_item and o.datasource_item['index'] == item_index)
    except StopIteration:
      # Fallback to input/reference matching
      try:
        output_item = next(o for o in output_items 
                          if o.datasource_item['input'].encode('utf-8', 'ignore').decode('utf-8').strip() == item['item']['input'].encode('utf-8', 'ignore').decode('utf-8').strip() 
                          and o.datasource_item['reference'].encode('utf-8', 'ignore').decode('utf-8').strip() == item['item']['reference'].encode('utf-8', 'ignore').decode('utf-8').strip())
      except StopIteration:
        print(f"    ERROR: No matching output found for input {idx + 1}: {truncate_string(item['item']['input'], 80)}")
        print(f"    FAILING: Evaluation run failed due to non-recoverable item")
        return items_copy, "FAIL"

    # Graceful retry mechanism to recover results
    max_result_retries = 10
    retry_delay = 10
    
    for retry_attempt in range(max_result_retries + 1):
      try:
        # Check if output_item has results
        if not output_item.results:
          if retry_attempt < max_result_retries:
            print(f"    WARNING: No results found for input {idx + 1} (attempt {retry_attempt + 1}/{max_result_retries + 1}). Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            # Re-fetch the output items to see if results have populated
            output_items = get_all_eval_run_output_items(client, run_id=eval_run.id, eval_id=eval_cfg.id, expected_count=len(items_copy), max_retries=3)
            # Re-find the matching output item
            try:
              output_item = next(o for o in output_items if 'index' in o.datasource_item and o.datasource_item['index'] == item_index)
            except StopIteration:
              try:
                output_item = next(o for o in output_items 
                                  if o.datasource_item['input'].encode('utf-8', 'ignore').decode('utf-8').strip() == item['item']['input'].encode('utf-8', 'ignore').decode('utf-8').strip() 
                                  and o.datasource_item['reference'].encode('utf-8', 'ignore').decode('utf-8').strip() == item['item']['reference'].encode('utf-8', 'ignore').decode('utf-8').strip())
              except StopIteration:
                print(f"    ERROR: Lost matching output during retry for input {idx + 1}")
                return items_copy, "FAIL"
            continue
          else:
            print(f"    ERROR: No results found for input {idx + 1} after {max_result_retries} retries")
            print(f"    FAILING: Evaluation run failed due to non-recoverable item")
            return items_copy, "FAIL"
        
        # Successfully found results - validate structure
        first_test_result = output_item.results[0]
        
        if 'score' not in first_test_result:
          if retry_attempt < max_result_retries:
            print(f"    WARNING: Invalid result structure for input {idx + 1} (attempt {retry_attempt + 1}/{max_result_retries + 1}). Retrying...")
            time.sleep(retry_delay)
            continue
          else:
            print(f"    ERROR: Invalid result structure for input {idx + 1} after retries")
            print(f"    FAILING: Evaluation run failed due to non-recoverable item")
            return items_copy, "FAIL"
        
        # Extract score and content with error handling
        score = first_test_result.get('score', -1)
        
        try:
          model_output_content = first_test_result['sample']['output'][0]['content']
        except (KeyError, IndexError, TypeError):
          if retry_attempt < max_result_retries:
            print(f"    WARNING: Cannot extract model output content for input {idx + 1} (attempt {retry_attempt + 1}/{max_result_retries + 1}). Retrying...")
            time.sleep(retry_delay)
            continue
          else:
            print(f"    ERROR: Cannot extract model output content for input {idx + 1} after retries")
            print(f"    FAILING: Evaluation run failed due to non-recoverable item")
            return items_copy, "FAIL"
        
        # Parse the JSON output and create rationale string from the steps
        try:
          output_json = json.loads(model_output_content)
          steps = output_json.get('steps', [])
          rationale = ["Conclusion: " + step.get('conclusion', 'N/A').replace('\n', ' ') + " Description: " + step.get('description', 'N/A').replace('\n', ' ') for step in steps]
          if not rationale:
            rationale = ["Successfully processed but no detailed steps available"]
        except json.JSONDecodeError:
          rationale = [f"Error parsing model output: {model_output_content[:100]}..."]
        
        # Successfully processed - update item and break retry loop
        item['item']['score'] = score
        item['item']['rationale'] = rationale
        
        if log_details:
          print(f"    Reference: {truncate_string(item['item']['reference'], 120)}")
          print(f"    Model output: {truncate_string(remove_linebreaks(item['item']['output_text']), 120)}")
          print(f"    Score: {score}")
          for r in rationale:
            print(f"      - {truncate_string(r, 140)}")
        
        break  # Success - exit retry loop
        
      except Exception as e:
        if retry_attempt < max_result_retries:
          print(f"    WARNING: Error processing input {idx + 1} (attempt {retry_attempt + 1}/{max_result_retries + 1}): {str(e)}. Retrying...")
          time.sleep(retry_delay)
          continue
        else:
          print(f"    ERROR: Failed to process input {idx + 1} after {max_result_retries} retries: {str(e)}")
          print(f"    FAILING: Evaluation run failed due to non-recoverable item")
          return items_copy, "FAIL"

  # Try delete evaluation after run if requested (can fail)
  if delete_eval_after_run:
      try: client.evals.delete(eval_id=eval_cfg.id)
      except: print(f"    WARNING: Failed to delete eval ID={eval_cfg.id}")

  log_function_footer(function_name, start_time)
  return items_copy, "OK"

# calculates the accuracy of the evaluation model by using the calibration Batch02 where each score has 10 reference answers + model outputs
# returns a string like this: Accuracy: 72%; Score 0: [9/10 = 90%], Score 1: [9/10 = 90%], Score 2: [9/10 = 90%], Score 3: [6/10 = 60%], Score 4: [9/10 = 90%], Score 5: [9/10 = 90%]
def analyze_batch02_scores_and_return_string(items):
  # Initialize counters for each score block
  # Group items by their target_score field instead of fixed slicing
  score_blocks = {}
  for item in items:
    target_score = item['item'].get('target_score')
    if target_score is not None:
      if target_score not in score_blocks:
        score_blocks[target_score] = []
      score_blocks[target_score].append(item)
  
  score_counts = {i: {'total': 0, 'correct': 0} for i in range(6)}
  total_items = 0; total_correct = 0

  # Process each group of items by target score
  for expected_score, block_items in score_blocks.items():
    for item in block_items:
      score = item['item']['score']
      score_counts[expected_score]['total'] += 1
      if score == expected_score: score_counts[expected_score]['correct'] += 1
      total_items += 1

  total_correct = sum(count['correct'] for count in score_counts.values())
  
  string_parts = []
  accuracy = (total_correct / total_items * 100) if total_items > 0 else 0
  string_parts.append(f"Batch02 accuracy: {accuracy:.0f}%")
  
  for score in range(6):
    correct = score_counts[score]['correct']; total = score_counts[score]['total']
    percentage = (correct / total * 100) if total > 0 else 0
    string_parts.append(f"Score {score}: [{correct}/{total} = {percentage:.0f}%]")
  
  return "; ".join(string_parts)

# creates score table and if items == Batch02 it also calculates the evaluation model accuracy
def summarize_item_scores(items, min_score: int, indentation: int = 0) -> str:
  # calculate average score
  scores = [item['item']['score'] for item in items if item['item'].get('score') is not None]
  # count all answers as correct that have min_score
  questions_answered_correctly = sum(1 for item in items if item['item'].get('score') is not None and item['item']['score'] >= min_score)
  questions_answered_correctly_percent = questions_answered_correctly / len(items)
  average_score = sum(scores) / len(scores) if scores else 0
  average_score_in_percent = average_score / 5
  indentation_string = " " * indentation
  
  max_chars_question = 20; max_chars_reference = 30; max_chars_answer = 30; max_chars_score = 6
  # Create output table
  table = "\n" + indentation_string + f"{'Question':{max_chars_question}} | {'Reference':{max_chars_reference}} | {'Answer':{max_chars_answer}} | {'Score':<{max_chars_score}}\n"
  table += indentation_string + "-" * (max_chars_question+max_chars_reference+max_chars_answer+max_chars_score+10)
  
  for item in items:
    question = item['item']['input'].replace("\n", " ")[:max_chars_question]
    reference = item['item']['reference'].replace("\n", " ")[:max_chars_reference]
    answer = item['item'].get('output_text', '').replace("\n", " ")[:max_chars_answer]
    score = item['item'].get('score', 'N/A')
    table += "\n" + indentation_string + f"{question:{max_chars_question}} | {reference:{max_chars_reference}} | {answer:{max_chars_answer}} | {str(score):<{max_chars_score}}"
  
  summary = indentation_string + analyze_batch02_scores_and_return_string(items) if items == Batch02 else ""
  summary += "\n" + indentation_string + f"{questions_answered_correctly} of {len(items)} answers correct ({questions_answered_correctly_percent:.0%}). Average score: {average_score:.2f} ({average_score_in_percent:.0%})."
  return  summary + table

# Print lines as box with + and - and | characters
def print_as_box(indentation: int, lines: str | list, min_width: int):
  # Convert single string to list
  if isinstance(lines, str): lines = [lines]
  # Calculate required width
  content_width = max(max(len(line) for line in lines), min_width)
  # Create top/bottom border with + at corners
  border = "+" + "-" * (content_width + 2) + "+"
  indent = " " * indentation
  # Print box
  print(f"{indent}{border}")
  for line in lines:
    right_pad = content_width - len(line)
    print(f"{indent}| {line}{' ' * right_pad} |")
  print(f"{indent}{border}")

# Check if items have the same questions as Batch02 by comparing input text
def is_same_as_batch02_items(items) -> bool:
  if len(items) != len(Batch02): return False
  for i, item in enumerate(items):
    if item['item']['input'] != Batch02[i]['item']['input']: return False
  return True

# Measures the variability of the score model by running the evaluation multiple times and calculating the standard deviation of the scores
def measure_score_model_variability(client, items, eval_name, prompt_template, eval_model, min_score: int, number_of_runs: int, remove_input_from_prompt: bool = False, delete_eval_after_run: bool = False, log_details: bool = True):
  function_name = 'Measure score model variability'
  start_time = log_function_header(function_name)
  
  # Make a deep copy of items to avoid modifying the original
  items_copy = copy.deepcopy(items)

  # Store scores for each item across all runs
  item_scores = {i: [] for i in range(len(items_copy))}

  # Run the evaluation multiple times
  successful_runs = 0
  for run in range(number_of_runs):
    print(f"-------------- Run {run + 1} of {number_of_runs} --------------")
    eval_name2 = f"{eval_name} - run {run + 1}"
    # Run evaluation and collect scores
    scored_items, status = score_answers_using_score_model_grader_and_return_items( client, items_copy, eval_name2, prompt_template, eval_model, min_score, remove_input_from_prompt, delete_eval_after_run, log_details=False)
    
    if status == "OK":
      successful_runs += 1
      for i, item in enumerate(scored_items):
        score = item['item']['score']
        item_scores[i].append(score)
    else:
      print(f"    SKIPPED: Run {run + 1} failed and will not be counted in variability analysis")
  
  if successful_runs == 0:
    print(f"  ERROR: All {number_of_runs} runs failed. Cannot perform variability analysis.")
    log_function_footer(function_name, start_time)
    return
  
  print(f"  SUMMARY: {successful_runs} of {number_of_runs} runs completed successfully")

  # Calculate metrics for each item
  unstable_score_items = 0;all_std_devs = []
  score_counts = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}  # Track items per score across runs
  above_min_score_100_percent = 0
  below_min_score_100_percent = 0
  pass_fail_unstable_items = 0
  
  for i, item in enumerate(items_copy):
    scores = item_scores[i]
    if scores:
      std = np.std(scores)
      score_range = (min(scores), max(scores))
      is_unstable = len(set(scores)) > 1
      if is_unstable: unstable_score_items += 1
      
      # Check if item consistently scores above or equal to min_score
      if all(score >= min_score for score in scores):
        above_min_score_100_percent += 1
      
      # Check if item consistently scores below min_score (fails 100% of runs)
      if all(score < min_score for score in scores):
        below_min_score_100_percent += 1
      
      # Check if item is unstable between pass/fail (has both scores >= min_score and < min_score)
      has_pass = any(score >= min_score for score in scores)
      has_fail = any(score < min_score for score in scores)
      if has_pass and has_fail:
        pass_fail_unstable_items += 1
            
      # Count occurrences of each score for this item
      for score in scores:
        if score in score_counts:
          score_counts[score].append(i)
      
      item['item']['score_variability'] = { 'scores': scores, 'std': std, 'min': score_range[0], 'max': score_range[1], 'unstable': is_unstable }
      all_std_devs.append(std)
  
  # Calculate average number of items per score
  avg_items_per_score = {}
  for score in range(6):
    avg_items_per_score[score] = len(score_counts[score]) / successful_runs if successful_runs > 0 else 0

  total_items = len(items_copy)
  scoring_stability = (total_items - unstable_score_items) / total_items if total_items > 0 else 0.0
  pass_fail_stability = (total_items - pass_fail_unstable_items) / total_items if total_items > 0 else 0.0
  avg_std_dev = np.mean(all_std_devs) if all_std_devs else 0.0
  magnitude_of_deviation = lambda avg_std_dev: "none" if avg_std_dev == 0 else "very low" if avg_std_dev < 0.05 else "low" if avg_std_dev < 0.15 else "moderate" if avg_std_dev < 0.4 else "high"

  # Calculate calibration accuracy if items are the same as Batch02 (our calibration dataset)
  ml_metrics = None
  if is_same_as_batch02_items(items_copy):
    expected_scores = [float(item['item']['target_score']) for item in items_copy]  # Get expected scores from target_score attributes
    
    # Calculate ML Classification Metrics
    all_predictions = []
    all_true_labels = []
    
    # Collect all predictions and true labels across all runs
    for i, expected_score in enumerate(expected_scores):
      if i in item_scores:
        for actual_score in item_scores[i]:
          
          # True label: 1 if should pass (expected >= min_score), 0 if should fail
          true_label = 1 if expected_score >= min_score else 0
          # Predicted label: 1 if predicted to pass (actual >= min_score), 0 if predicted to fail
          predicted_label = 1 if actual_score >= min_score else 0
          
          all_predictions.append(predicted_label)
          all_true_labels.append(true_label)
    
    # Calculate confusion matrix components
    tp = sum(1 for pred, true in zip(all_predictions, all_true_labels) if pred == 1 and true == 1)  # True Positives
    fp = sum(1 for pred, true in zip(all_predictions, all_true_labels) if pred == 1 and true == 0)  # False Positives
    fn = sum(1 for pred, true in zip(all_predictions, all_true_labels) if pred == 0 and true == 1)  # False Negatives
    tn = sum(1 for pred, true in zip(all_predictions, all_true_labels) if pred == 0 and true == 0)  # True Negatives
    
    # Calculate ML metrics
    total_predictions = len(all_predictions)
    accuracy = (tp + tn) / total_predictions if total_predictions > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Store metrics for output
    ml_metrics = {
      'accuracy': accuracy * 100,
      'precision': precision * 100,
      'recall': recall * 100,
      'f1_score': f1_score * 100,
      'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
      'total_predictions': total_predictions
    }

  content_lines = [
    f"Variability statistics for {number_of_runs} runs of '{eval_name}', model '{eval_model}':",
    "-" * 100,
  ]  
 
  content_lines.extend([
    f"Pass/Fail Stability (higher = better)               : {pass_fail_stability * 100:5.1f}% ( {total_items - pass_fail_unstable_items} / {total_items} items, {pass_fail_unstable_items} unstable )",
    f"Scoring Stability (higher = better)                 : {scoring_stability * 100:5.1f}% ( {total_items - unstable_score_items} / {total_items} items )",
    f"Average Standard Deviation                          :  {avg_std_dev:.2f} ( {magnitude_of_deviation(avg_std_dev)} )",
    f"Items passing 100% of runs (score >= {min_score})             : {above_min_score_100_percent/total_items*100:5.1f}% ( {above_min_score_100_percent} / {total_items} items )",
    f"Items failing 100% of runs (score < {min_score})              : {below_min_score_100_percent/total_items*100:5.1f}% ( {below_min_score_100_percent} / {total_items} items )",
  ])
  
  # Add ML Classification metrics if applicable
  if ml_metrics is not None:
    content_lines.extend([
      f"----- Batch02 Classification Metrics (threshold: score >= {min_score}) -----",
      f"  Accuracy (% of all correct predictions)           : {ml_metrics['accuracy']:6.1f}% ( {ml_metrics['tp'] + ml_metrics['tn']} / {ml_metrics['total_predictions']} correct predictions )",
      f"  Precision (% of predicted passes are passes)      : {ml_metrics['precision']:6.1f}% ( {ml_metrics['tp']} / {ml_metrics['tp'] + ml_metrics['fp']} when predicted pass )",
      f"  Recall (% of real passes that were found)         : {ml_metrics['recall']:6.1f}% ( {ml_metrics['tp']} / {ml_metrics['tp'] + ml_metrics['fn']} actual passes found )",
      f"  F1 Score (balance of precision & recall)          : {ml_metrics['f1_score']:6.1f}% ( harmonic mean of precision & recall )",
      f"  Confusion Matrix                                  : TP={ml_metrics['tp']}, FP={ml_metrics['fp']}, FN={ml_metrics['fn']}, TN={ml_metrics['tn']}",
    ])
  
  content_lines.append(f"Average number of items: Score 0: {avg_items_per_score[0]:.1f},  Score 1: {avg_items_per_score[1]:.1f}, Score 2: {avg_items_per_score[2]:.1f}, Score 3: {avg_items_per_score[3]:.1f}, Score 4: {avg_items_per_score[4]:.1f}, Score 5: {avg_items_per_score[5]:.1f}")
  print_as_box(0, content_lines, 60)
  
  log_function_footer(function_name, start_time)
  return items_copy, "OK"

def log_eval_items_to_file(items, log_filename, log_dir):  
  # Create log directory if it doesn't exist
  os.makedirs(log_dir, exist_ok=True)  
  # Generate filename with timestamp and vector store ID
  log_filepath = os.path.join(log_dir, log_filename)
  # Convert to absolute path
  absolute_log_filepath = os.path.abspath(log_filepath)
  # Save model outputs to JSON file
  with open(log_filepath, 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
  print(f"Model outputs logged to: '{absolute_log_filepath}'.")

# ----------------------------------------------------- END: Tests ------------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  if openai_service_type == "openai":
    answer_model_name = "gpt-5-nano"
    eval_model_name = "gpt-4o"
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    answer_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    eval_model_name = os.getenv("AZURE_OPENAI_EVAL_MODEL_DEPLOYMENT_NAME", "gpt-4o")
    azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class EvalParams: vector_store_name: str; folder_path: str; eval_path: str; items: list; answer_model: str; eval_model: str; instructions: str; answer_temperature: int; answer_reasoning_effort: str; embedding_model: str; min_score: int; remove_input_from_prompt: bool; delete_eval_after_run: bool; log_details: bool; log_model_output: bool; log_eval_output: bool; variability_runs: int

  eval_log_folder_path = "./eval-logs"

  params = EvalParams(
    vector_store_name="test_vector_store"
    ,folder_path="./RAGFiles/Batch01"
    # if you have a path to a JSON file with items, the code will load the items from the file instead of using the assigned batch objects
    ,eval_path=None 
    ,items = Batch01
    ,answer_model = answer_model_name
    ,eval_model = eval_model_name
    ,instructions = None
    ,answer_temperature=0
    ,answer_reasoning_effort="low"
    ,embedding_model="text-embedding-3-small"
    ,min_score=4
    # By removing the input from the evaluation prompt templates we can demonstrate that evaluation needs the input to be able to provide a correct evaluation
    # CORRECT   -> reference="Jupiter" vs. output="Zeus" for input="Who is the master of the olympian gods?"
    # INCORRECT -> reference="Jupiter" vs. output="Zeus" for input="What is largest planet in our solar system?"
    ,remove_input_from_prompt=False
    ,delete_eval_after_run=False
    ,log_details=True
    ,log_model_output=True
    ,log_eval_output=True
    ,variability_runs=1
  )

  # If we have path to eval file, load items from eval file (JSON)
  if params.eval_path:
    with open(params.eval_path, 'r') as f:
      eval_data = json.load(f)
      params.items = eval_data
      # params.items = [item['item'] for item in eval_data]

  # If re_create_vector_store_and_get_model_outputs=True, create temporary vector store by uploading files and get answers from model
  re_create_vector_store_and_get_model_outputs = False
  if re_create_vector_store_and_get_model_outputs:
    print("-"*140)
    # Step 1: Create vector store by uploading files
    test_vector_store_with_files = create_test_vector_store_from_folder_path(client,params.vector_store_name, params.folder_path)
    print("-"*140)
    # Step 2: Get answers from model and store in items
    params.items = get_answers_from_model_and_return_items(client, test_vector_store_with_files.vector_store.id, params.answer_model, params.items)
    print("-"*140)
  
  # If use_existing_vector_store_and_get_model_outputs=True, uses existing vector store to get answers from model
  use_existing_vector_store_and_get_model_outputs = True
  if use_existing_vector_store_and_get_model_outputs:
    vector_store_name = "test_vector_store"; vector_store_id = None
    if vector_store_id: vs = get_vector_store_by_id(client, vector_store_id)
    elif vector_store_name: vs = get_vector_store_by_name(client, vector_store_name)
    else: raise Exception("No vector store id or name provided")
    if vs is None: raise Exception(f"Vector store '{vector_store_name}' not found. Please create it first or check the name.")
    
    print("-"*140)    
    # Step 1: Get answers from model and store in items
    params.items, status = get_answers_from_model_and_return_items(client, vs.id, params.answer_model, params.items, params.instructions, params.answer_temperature, params.answer_reasoning_effort)
    print("-"*140)

  # Log model output in "../eval-logs/[DATETIME]_[VSID]_modeloutputs.json"
  if params.log_model_output:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = f"{timestamp}_{vs.id}_modeloutputs.json"
    log_eval_items_to_file(params.items, log_filename, eval_log_folder_path)

  # Step 3A: Test eval using embedding and cosine similarity
  params.items, status = score_answers_using_cosine_similarity_and_return_items(client, params.items, params.embedding_model, params.log_details)
  print("."*100 + f"\n    Evaluation results using embedding with '{params.embedding_model}' and cosine similiarity:")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)
  # Step 3B: Test eval using judge model with prompt template 1 (Simple)
  params.items, status = score_answers_using_judge_model_and_return_items(client, params.items, judge_model_prompt_template_1, params.eval_model, params.remove_input_from_prompt, params.log_details)
  print("."*100 + f"\n    Evaluation results using judge model '{params.eval_model}' with prompt template 1 (Simple):")
  print(summarize_item_scores(params.items, params.min_score, 4) )
  print("-"*140)
  # Step 3C: Test eval using judge model with prompt template 2 (Scoring Model)
  params.items, status = score_answers_using_judge_model_and_return_items(client, params.items, judge_model_prompt_template_2, params.eval_model, params.remove_input_from_prompt, params.log_details)
  print("."*100 + f"\n    Evaluation results using judge model '{params.eval_model}' with prompt template 2 (Scoring Model):")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)
  # Step 3D: Test eval using score model grader with prompt template 1 (Simple)
  params.items, status = score_answers_using_score_model_grader_and_return_items(client, params.items, "test_eval - prompt_template_1", judge_model_prompt_template_1, params.eval_model, params.min_score, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  print("."*100 + f"\n    Evaluation results using 'score_model' grader and prompt template 1 (Simple):")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)
  # Step 3E: Test eval using score model grader with prompt template 2 (Scoring Model)
  params.items, status = score_answers_using_score_model_grader_and_return_items(client, params.items, "test_eval - prompt_template_2", judge_model_prompt_template_2, params.eval_model, params.min_score, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  print("."*100 + f"\n    Evaluation results using 'score_model' grader and prompt template 2 (Scoring Model):")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)
  # Step 3F: Test eval using score model grader with prompt template 3 (Langchain Correctness)
  params.items, status = score_answers_using_score_model_grader_and_return_items(client, params.items, "test_eval - prompt_template_3", judge_model_prompt_template_3, params.eval_model, params.min_score, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  print("."*100 + f"\n    Evaluation results using 'score_model' grader and prompt template 3 (Langchain Correctness):")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)

  # params.items, status = score_answers_using_score_model_grader_and_return_items(client, params.items, "eval - azure similarity", judge_model_prompt_template_5, params.eval_model, params.min_score, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("."*100 + f"\n    Evaluation results using 'score_model' grader and prompt template 5 (Azure Similarity):")
  # print(summarize_item_scores(params.items, params.min_score, 4))
  # print("-"*140)

  # Log eval output in "../eval-logs/[DATETIME]_[VSID]_evaloutputs.json"
  if params.log_eval_output:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = f"{timestamp}_{vs.id}_evaloutputs.json"
    log_eval_items_to_file(params.items, log_filename, eval_log_folder_path)

  # # Step 4A: Measure variablity of prompt 1
  # measure_score_model_variability(client, params.items, "Eval Prompt 1 (Simple)", judge_model_prompt_template_1, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)
  # # Step 4B: Measure variablity of prompt 2
  # measure_score_model_variability(client, params.items, "Eval Prompt 2 (Math Scoring Model B)", judge_model_prompt_template_2, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)
  # # Step 4C: Measure variablity of prompt 3
  # measure_score_model_variability(client, params.items, "Eval Prompt 3 (Langchain Correctness)", judge_model_prompt_template_3, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)
  # # Step 4D: Measure variablity of prompt 4
  # measure_score_model_variability(client, params.items, "Eval Prompt 4 (AI Foundry Semantic Similarity)", judge_model_prompt_template_4, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)
  # # Step 4E: Measure variablity of prompt 5
  # measure_score_model_variability(client, params.items, "Eval Prompt 5 (AI Foundry Similarity)", judge_model_prompt_template_5, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)
  # # Step 4F: Measure variablity of prompt 6
  # measure_score_model_variability(client, params.items, "Eval Prompt 6 (LlamaIndex Correctness)", judge_model_prompt_template_6, params.eval_model, params.min_score, params.variability_runs, params.remove_input_from_prompt, params.delete_eval_after_run, params.log_details)
  # print("-"*140)

  # Step 4: Delete vector store including all files
  if re_create_vector_store_and_get_model_outputs: delete_vector_store_by_name(client, params.vector_store_name)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
