import csv

# Sections for each chapter/topic
sections = [
    "Key Concepts and Theory",
    "Quiz",
    "Midterm Exam",
    "Short Notes",
    "Exemplar Problems",
    "Exam Prep"
]

# CBSE Classes and Subjects -- condensed for script size; expand as needed!
cbse_syllabus = {
    "Class 6": {
        "Science": [
            "Food: Where Does It Come From?",
            "Components of Food",
            "Fibre to Fabric",
            "Sorting Materials into Groups",
            "Separation of Substances",
            "Changes Around Us",
            "Getting to Know Plants",
            "Body Movements",
            "The Living Organisms and Their Surroundings",
            "Motion and Measurement of Distances",
            "Light, Shadows and Reflections",
            "Electricity and Circuits",
            "Fun with Magnets",
            "Water",
            "Air Around Us",
            "Garbage In, Garbage Out"
        ],
        "Maths": [
            "Knowing Our Numbers",
            "Whole Numbers",
            "Playing with Numbers",
            "Basic Geometrical Ideas",
            "Understanding Elementary Shapes",
            "Integers",
            "Fractions",
            "Decimals",
            "Data Handling",
            "Mensuration",
            "Algebra",
            "Ratio and Proportion",
            "Symmetry",
            "Practical Geometry"
        ],
        "Social Science": [
            # History
            "What, Where, How and When?",
            "On the Trail of the Earliest People",
            "From Gathering to Growing Food",
            "In the Earliest Cities",
            "What Books and Burials Tell Us",
            # Geography
            "The Earth in the Solar System",
            "Globe: Latitudes and Longitudes",
            "Motions of the Earth",
            "Maps",
            "Major Domains of the Earth",
            "Major Landforms of the Earth",
            "Our Country - India",
            "India: Climate, Vegetation and Wildlife"
        ],
        "English": [
            "Who Did Patrick’s Homework?",
            "How the Dog Found Himself a New Master!",
            "Taro’s Reward",
            "An Indian-American Woman in Space",
            "A Different Kind of School"
            # ...more chapters
        ],
        "Hindi": [
            "वह चिड़िया जो",
            "बचपन",
            "नादान दोस्त",
            "चाँद से थोड़ी सी गप्पे",
            "आसपास"
            # ...more chapters
        ]
    },
    "Class 7": {
        "Science": [
            "Nutrition in Plants",
            "Nutrition in Animals",
            "Fibre to Fabric",
            "Heat",
            "Acids, Bases and Salts",
            "Physical and Chemical Changes",
            "Weather, Climate and Adaptations of Animals",
            "Winds, Storms and Cyclones",
            "Soil",
            "Respiration in Organisms",
            "Transportation in Animals and Plants",
            "Reproduction in Plants",
            "Motion and Time",
            "Electric Current and its Effects",
            "Light",
            "Water: A Precious Resource",
            "Forests: Our Lifeline",
            "Wastewater Story"
        ],
        "Maths": [
            "Integers",
            "Fractions and Decimals",
            "Data Handling",
            "Simple Equations",
            "Lines and Angles",
            "Triangles and Their Properties",
            "Congruence of Triangles",
            "Comparing Quantities",
            "Rational Numbers",
            "Practical Geometry",
            "Perimeter and Area",
            "Algebraic Expressions",
            "Exponents and Powers",
            "Symmetry",
            "Visualising Solid Shapes"
        ],
        # ... Social Science, English, Hindi chapters similarly
    },
    "Class 8": {
        "Science": [
            "Crop Production and Management",
            "Microorganisms: Friend and Foe",
            "Synthetic Fibres and Plastics",
            "Materials: Metals and Non-Metals",
            "Coal and Petroleum",
            "Combustion and Flame"
            # ...
        ],
        # ...
    },
    # Expand similarly for Class 9, 10, 11, 12 (use NCERT lists)
}

# Add "top 5" government exams with representative syllabus/topics
govt_exams = {
    "SSC": {
        "Quantitative Aptitude": [
            "Number System",
            "Algebra",
            "Percentage",
            "Profit and Loss",
            "Ratio & Proportion"
        ],
        "Reasoning": [
            "Analogy",
            "Coding-Decoding",
            "Series",
            "Blood Relations",
            "Syllogism"
        ],
        "General Awareness": [
            "History",
            "Geography",
            "Polity",
            "Economics",
            "Current Affairs"
        ],
        "English": [
            "Reading Comprehension",
            "Grammar",
            "Cloze Test",
            "Error Spotting"
        ]
    },
    "Banking": {
        "Quantitative Aptitude": [
            "Simplification",
            "Number Series",
            "Data Interpretation",
            "Quadratic Equations"
        ],
        "Reasoning": [
            "Puzzles",
            "Sitting Arrangement",
            "Inequality"
        ],
        "English": [
            "Cloze Test",
            "Reading Comprehension",
            "Sentence Improvement"
        ],
        "General Awareness": [
            "Banking Awareness",
            "Current Affairs"
        ],
        "Computer Knowledge": [
            "Basics of Computers"
        ]
    },
    "Railways": {
        "Mathematics": [
            "Number System",
            "Algebra",
            "Geometry"
        ],
        "General Intelligence & Reasoning": [
            "Analogies",
            "Coding-Decoding"
        ],
        "General Awareness": [
            "Indian History",
            "Geography"
        ],
        "General Science": [
            "Physics",
            "Chemistry",
            "Biology"
        ]
    },
    "Civil Services": {
        "General Studies I": [
            "Indian History",
            "Polity",
            "Geography",
            "Economy",
            "Environment",
            "Current Affairs"
        ],
        "CSAT": [
            "Quantitative Aptitude",
            "Reasoning Ability",
            "English Comprehension"
        ]
    },
    "Teaching": {
        "Child Development & Pedagogy": [
            "Learning Theories",
            "Assessment"
        ],
        "Mathematics": [
            "Arithmetic",
            "Geometry"
        ],
        "EVS": [
            "Plants",
            "Environment"
        ],
        "Language I": [
            "Reading Comprehension",
            "Grammar"
        ],
        "Language II": [
            "Reading Comprehension",
            "Grammar"
        ]
    }
}

# Start writing
with open("cbse_govt_exam_master_structure.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Course", "Chapter", "Section"])
    
    # CBSE Classes
    for cls, subjects in cbse_syllabus.items():
        for subj, chapters in subjects.items():
            for ch in chapters:
                for sec in sections:
                    writer.writerow([f"CBSE {cls}", f"{cls} {subj}", ch, sec])
    
    # Government Exams
    for exam, courses in govt_exams.items():
        for course, chapters in courses.items():
            for ch in chapters:
                for sec in sections:
                    writer.writerow([exam, course, ch, sec])

print("CSV file 'cbse_govt_exam_master_structure.csv' has been generated.")

