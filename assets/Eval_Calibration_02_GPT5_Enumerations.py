Batch02 = [
  # Strategy 0 – Completely wrong
  { "item": { "input": "What is the derivative of x^2?", "reference": "The derivative of x^2 is 2x.", "output_text": "" } }
  ,{ "item": { "input": "Where does photosynthesis occur in living organisms?", "reference": "Photosynthesis occurs in the chloroplasts of plant cells and some protists.", "output_text": "Photosynthesis occurs in animal liver cells." } }
  ,{ "item": { "input": "Explain recursion in programming.", "reference": "Recursion is when a function calls itself directly or indirectly to solve a problem.", "output_text": "Inflation affects currency value and purchasing power." } }
  ,{ "item": { "input": "Define GDP in economics.", "reference": "Gross Domestic Product (GDP) is the total monetary value of all goods and services produced within a country's borders in a given period.", "output_text": "A loop runs until a condition is false." } }
  ,{ "item": { "input": "Who wrote 'Hamlet'?", "reference": "'Hamlet' was written by William Shakespeare.", "output_text": "Shakespeare wrote The Theory of Relativity." } }
  ,{ "item": { "input": "What is the value of pi to two decimal places?", "reference": "3.14", "output_text": "Pi is exactly 4." } }
  ,{ "item": { "input": "List the stages of mitosis.", "reference": "The stages of mitosis are prophase, metaphase, anaphase, and telophase.", "output_text": "Teamwork is important for success." } }
  ,{ "item": { "input": "What is the law of supply and demand?", "reference": "The law of supply and demand states that the price of a good is determined by the relationship between its supply and demand.", "output_text": "Happiness is key to a good life." } }
  ,{ "item": { "input": "Name the primary colors of light.", "reference": "The primary colors of light are red, green, and blue.", "output_text": "" } }
  ,{ "item": { "input": "What is Newton's first law of motion?", "reference": "An object will remain at rest or move in a straight line at constant speed unless acted upon by an external force.", "output_text": "I don't know." } }

  # Strategy 1.1 – One fact, rest wrong
  ,{ "item": { "input": "List five prime numbers.", "reference": "Examples of prime numbers are 2, 3, 5, 7, 11.", "output_text": "2, 4, 6, 8, 10." } }
  ,{ "item": { "input": "Name five major human organs.", "reference": "Five major human organs are heart, lungs, liver, kidneys, and brain.", "output_text": "Heart, rock, paper, pen, shoe." } }
  # Strategy 1.2 – One correct conclusion, wrong facts
  ,{ "item": { "input": "List five principles of object-oriented programming.", "reference": "The five principles are encapsulation, inheritance, abstraction, polymorphism, and composition.", "output_text": "Inheritance, banana, chair, table, sky." } }
  ,{ "item": { "input": "Name five plays by William Shakespeare.", "reference": "Five plays are Hamlet, Macbeth, Othello, King Lear, and Romeo and Juliet.", "output_text": "Hamlet, Sunflower, Car, Beach, Moon." } }
  # Strategy 1.3 – Correct terminology but wrong linkage
  ,{ "item": { "input": "How is GDP calculated?", "reference": "GDP is calculated by summing consumption, investment, government spending, and net exports.", "output_text": "GDP is calculated by adding inflation to unemployment." } }
  ,{ "item": { "input": "What is DNA?", "reference": "DNA is a molecule that carries genetic instructions in all living organisms.", "output_text": "DNA is a type of protein." } }
  # Strategy 1.4 – Only defines the topic
  ,{ "item": { "input": "List five types of triangles.", "reference": "Equilateral, isosceles, scalene, acute, and obtuse.", "output_text": "A triangle has three sides." } }
  ,{ "item": { "input": "List five Python data types.", "reference": "Python data types include int, float, str, list, and dict.", "output_text": "Python is a programming language." } }
  # Strategy 1.5 – Partially copied but distorted
  ,{ "item": { "input": "Name five plays by Shakespeare.", "reference": "Hamlet, Macbeth, Othello, King Lear, Romeo and Juliet.", "output_text": "Hamlet, Macbeth, Chair, Leaf, Star." } }
  ,{ "item": { "input": "List five causes of inflation.", "reference": "Causes include demand-pull inflation, cost-push inflation, monetary expansion, supply shocks, and expectations.", "output_text": "Inflation, Moonlight, Taxes, Bird, Snow." } }

  # Strategy 2.1 – Two correct items, others wrong
  ,{ "item": { "input": "List five prime numbers.", "reference": "Examples of prime numbers are 2, 3, 5, 7, 11.", "output_text": "2, 3, 9, 12, 15." } }
  ,{ "item": { "input": "Name five major human organs.", "reference": "Five major human organs are heart, lungs, liver, kidneys, and brain.", "output_text": "Heart, lungs, chair, shoe, tree." } }
  # Strategy 2.2 – Two correct conclusions, missing others
  ,{ "item": { "input": "List five principles of object-oriented programming.", "reference": "The five principles are encapsulation, inheritance, abstraction, polymorphism, and composition.", "output_text": "Encapsulation, inheritance, car, road, water." } }
  ,{ "item": { "input": "Name five key concepts in economics.", "reference": "Supply, demand, inflation, opportunity cost, and market equilibrium.", "output_text": "Supply, demand, cloud, pencil, stone." } }
  # Strategy 2.3 – Correct facts but wrong extra claims
  ,{ "item": { "input": "List five plays by William Shakespeare.", "reference": "Hamlet, Macbeth, Othello, King Lear, Romeo and Juliet.", "output_text": "Hamlet, Macbeth, The Car, The Table, Sky Nights." } }
  ,{ "item": { "input": "Name five molecules essential for life.", "reference": "DNA, RNA, proteins, carbohydrates, lipids.", "output_text": "DNA, RNA, Coal, Wood, Metal." } }
  # Strategy 2.4 – Partial definitions for two items
  ,{ "item": { "input": "List five geometric shapes.", "reference": "Square, triangle, pentagon, hexagon, octagon.", "output_text": "A square has four sides, a triangle has three sides, and some other shapes exist." } }
  ,{ "item": { "input": "List five Python data types.", "reference": "int, float, str, list, dict.", "output_text": "Python supports lists and dictionaries, plus other things." } }
  # Strategy 2.5 – Two correct facts but disorganized
  ,{ "item": { "input": "Name five economic indicators.", "reference": "GDP, inflation rate, unemployment rate, interest rate, consumer confidence index.", "output_text": "GDP… banana… unemployment… cloud… tax." } }
  ,{ "item": { "input": "Name five plays by Shakespeare.", "reference": "Hamlet, Macbeth, Othello, King Lear, Romeo and Juliet.", "output_text": "Romeo and Juliet, Macbeth… sky… door… love." } }

  # Strategy 3.1 – Three correct, two wrong
  ,{ "item": { "input": "List five types of triangles.", "reference": "Equilateral, isosceles, scalene, acute, and obtuse.", "output_text": "Equilateral, isosceles, scalene, right, circle." } }
  ,{ "item": { "input": "Name five major human organs.", "reference": "Heart, lungs, liver, kidneys, and brain.", "output_text": "Heart, lungs, liver, rock, shoe." } }
  # Strategy 3.2 – Three correct conclusions, missing others
  ,{ "item": { "input": "List five principles of object-oriented programming.", "reference": "Encapsulation, inheritance, abstraction, polymorphism, and composition.", "output_text": "Encapsulation, inheritance, polymorphism." } }
  ,{ "item": { "input": "Name five key concepts in economics.", "reference": "Supply, demand, inflation, opportunity cost, and market equilibrium.", "output_text": "Supply, demand, inflation." } }
  # Strategy 3.3 – Accurate 3 facts + 2 vague placeholders
  ,{ "item": { "input": "Name five Shakespearean tragedies.", "reference": "Hamlet, Macbeth, Othello, King Lear, and Romeo and Juliet.", "output_text": "Hamlet, Macbeth, Othello, some others, various plays." } }
  ,{ "item": { "input": "List five stages of cellular respiration.", "reference": "Glycolysis, pyruvate oxidation, Krebs cycle, electron transport chain, and oxidative phosphorylation.", "output_text": "Glycolysis, Krebs cycle, electron transport chain, other steps, etc." } }
  # Strategy 3.4 – Three facts correct but slightly mis-termed
  ,{ "item": { "input": "List five fundamental properties of real numbers.", "reference": "Commutative, associative, distributive, identity, and inverse properties.", "output_text": "Commutative, associative, distributive, unity property, annihilator property." } }
  ,{ "item": { "input": "Name five common market structures.", "reference": "Perfect competition, monopolistic competition, oligopoly, monopoly, and duopoly.", "output_text": "Perfect competition, oligopoly, monopoly, free market, trade deficit." } }
  # Strategy 3.5 – 3 correct facts but mixed order & logic
  ,{ "item": { "input": "List five common HTTP methods.", "reference": "GET, POST, PUT, DELETE, and PATCH.", "output_text": "GET, POST, PUT, for-loop, while-loop." } }
  ,{ "item": { "input": "Name five major English Romantic poets.", "reference": "Wordsworth, Coleridge, Byron, Shelley, and Keats.", "output_text": "Wordsworth, Keats, Byron, plot, meter." } }

  # Strategy 4.1 – Four correct, one wrong
  ,{ "item": { "input": "List five prime numbers.", "reference": "Examples of prime numbers are 2, 3, 5, 7, 11.", "output_text": "2, 3, 5, 7, 9." } }
  ,{ "item": { "input": "Name five major human organs.", "reference": "Heart, lungs, liver, kidneys, and brain.", "output_text": "Heart, lungs, liver, kidneys, shoe." } }
  # Strategy 4.2 – Four correct, one vague placeholder
  ,{ "item": { "input": "List five principles of object-oriented programming.", "reference": "Encapsulation, inheritance, abstraction, polymorphism, and composition.", "output_text": "Encapsulation, inheritance, abstraction, polymorphism, another one." } }
  ,{ "item": { "input": "Name five key concepts in economics.", "reference": "Supply, demand, inflation, opportunity cost, and market equilibrium.", "output_text": "Supply, demand, inflation, opportunity cost, something else." } }
  # Strategy 4.3 – Four correct, one mis-termed
  ,{ "item": { "input": "Name five Shakespearean tragedies.", "reference": "Hamlet, Macbeth, Othello, King Lear, and Romeo and Juliet.", "output_text": "Hamlet, Macbeth, Othello, King Lear, Romeo vs Juliet." } }
  ,{ "item": { "input": "List five cell organelles and their functions.", "reference": "Nucleus (stores DNA), mitochondria (produce energy), ribosomes (synthesize proteins), endoplasmic reticulum (processes proteins/lipids), Golgi apparatus (packages molecules).", "output_text": "Nucleus, mitochondria, ribosomes, ER, cell-maker." } }
  # Strategy 4.4 – Four correct + mild unsupported claim
  ,{ "item": { "input": "List five economic indicators.", "reference": "GDP, inflation rate, unemployment rate, interest rate, consumer confidence index.", "output_text": "GDP, inflation, unemployment, interest rate, blockchain mining." } }
  ,{ "item": { "input": "List five common polygons.", "reference": "Triangle, square, pentagon, hexagon, octagon.", "output_text": "Triangle, square, pentagon, hexagon, invisigon." } }
  # Strategy 4.5 – Four correct, missing depth for one
  ,{ "item": { "input": "List five Python data types.", "reference": "int, float, str, list, dict.", "output_text": "int, float, str, list, complex data." } }
  ,{ "item": { "input": "Name five major systems in the human body.", "reference": "Circulatory, respiratory, digestive, nervous, and skeletal systems.", "output_text": "Circulatory, respiratory, digestive, nervous, body system." } }

  # Strategy 5.1 – Exact match to reference but rephrased
  ,{ "item": { "input": "List five prime numbers.", "reference": "Examples of prime numbers are 2, 3, 5, 7, 11.", "output_text": "Five prime numbers include 2, 3, 5, 7, and 11." } }
  ,{ "item": { "input": "Name five major human organs.", "reference": "Heart, lungs, liver, kidneys, and brain.", "output_text": "Key organs are the heart, lungs, liver, kidneys, and the brain." } }
  # Strategy 5.2 – Perfect paraphrase
  ,{ "item": { "input": "List five principles of object-oriented programming.", "reference": "Encapsulation, inheritance, abstraction, polymorphism, and composition.", "output_text": "Core OOP principles include encapsulation, inheritance, abstraction, polymorphism, and composition." } }
  ,{ "item": { "input": "Name five key concepts in economics.", "reference": "Supply, demand, inflation, opportunity cost, and market equilibrium.", "output_text": "Economics rests on supply, demand, inflation, opportunity cost, and market equilibrium." } }
  # Strategy 5.3 – Perfect with examples
  ,{ "item": { "input": "Name five Shakespearean tragedies.", "reference": "Hamlet, Macbeth, Othello, King Lear, and Romeo and Juliet.", "output_text": "Famous tragedies by Shakespeare include Hamlet, Macbeth, Othello, King Lear, and Romeo and Juliet." } }
  ,{ "item": { "input": "List five cell organelles and their functions.", "reference": "Nucleus (stores DNA), mitochondria (produce energy), ribosomes (synthesize proteins), endoplasmic reticulum (processes proteins/lipids), Golgi apparatus (packages molecules).", "output_text": "The cell contains the nucleus for DNA storage, mitochondria for energy production, ribosomes for protein synthesis, the ER for processing, and the Golgi for packaging." } }
  # Strategy 5.4 – Perfect with synonyms
  ,{ "item": { "input": "List five economic indicators.", "reference": "GDP, inflation rate, unemployment rate, interest rate, consumer confidence index.", "output_text": "Major indicators are gross domestic product, rate of inflation, joblessness rate, interest rates, and consumer confidence." } }
  ,{ "item": { "input": "List five common polygons.", "reference": "Triangle, square, pentagon, hexagon, octagon.", "output_text": "Examples of polygons are triangle, square, pentagon, hexagon, and octagon." } }
  # Strategy 5.5 – Perfect + expanded context
  ,{ "item": { "input": "List five Python data types.", "reference": "int, float, str, list, dict.", "output_text": "Python offers several data types, such as integers, floating-point numbers, strings, lists, and dictionaries." } }
  ,{ "item": { "input": "Name five major systems in the human body.", "reference": "Circulatory, respiratory, digestive, nervous, and skeletal systems.", "output_text": "The human body is organized into systems including circulatory, respiratory, digestive, nervous, and skeletal." } }
]
