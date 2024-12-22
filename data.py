usage_guide_text = """

MathAssistant User Guide

Introduction:
    The MathAssistant 2.0 is an upgraded program purposed to help get better at Math. It provides a range of functionalities to assist with mathematical tasks, including interactive games, explanations of math topics, and random facts, saving sessions. This guide will walk you through how to use each feature effectively.

Features:

    Options:
        Usage Guide 📃
            Keys: '0', 'use'
            Shows the usage guide.

        Games 🎮
            Keys: '1', 'game'
            This option contains 2 games:
                Calculation Game
                    Generates various calculation expressions (addition, subtraction, multiplication, division).
                Guess Person Game
                    Provides information about a person related to math. You must guess their name.
                        Note: Enter the entire name without mistakes in a case-insensitive manner.
            Game Selection Keys:
                Calculation: 'c', 'calculate', 'calculating', 'calculation'
                Guess Person: 'g', 'guess', 'guessing'
                Return to Main Menu: 'b', 'back' or 'Ctrl+D' (Windows) / 'Ctrl+Z' (Linux/macOS)
            Additional Keys in Each Game:
                'a' or 'answer' in a case-insensitive manner.
                Return to Games Menu: 'b', 'back' or 'Ctrl+D' (Windows) / 'Ctrl+Z' (Linux/macOS)

        Random Fact 🎁
            Keys: '2', 'fact'
            Prints a random fact about math.

            
        Chat🗨️
            Keys: '3', 'chat'
            It is a chat with neural network assistant, which is using openai assistant api to generate responses
        
        Close Current Session 👋
            Keys: '4', 'exit', 'close', 'session'
            Asks if you want to save the session:
                If 'yes', you need to enter the file format ('PDF' or 'TXT') and filename in a case-insensitive manner.
                    If the file already exists, you will be asked if you want to replace the existing data.
                    If 'no', you will be asked for the filename again.
                After closing the session, you will see a cow saying 'Auf Wiedersehen' (Goodbye).
            Note: To return to the Main Menu, you can use 'Ctrl+D' (Windows) or 'Ctrl+Z' (Linux/macOS).

Additional Notes:
    1. Your input may contain multiple keys, but the first one will be used.
    2. If your input does not contain any key, you will receive an error message.
    3. You can enter keys in a case-insensitive manner.
    4. For 'yes/no' prompts, you can use 'Y' or 'Yes' for 'yes' and anything else for 'no'.
    5. You can always return to the Main Menu, Games Menu, or close the program using 'Ctrl+D' (Windows) or 'Ctrl+Z' (Linux/macOS).
"""

facts =  [
    "Zero is the only number that can't be represented in Roman numerals.",
    "Pi (π) is an irrational number - its decimal representation goes on forever without repeating.",
    "Euler's identity, e^{iπ} + 1 = 0, is often considered the most beautiful equation in mathematics.",
    "A 'googol' is the digit 1 followed by 100 zeros.",
    "A 'googolplex' is the digit 1 followed by a googol zeros.",
    "The Fibonacci sequence appears in nature, such as in the arrangement of leaves, flowers, and pinecones.",
    "The number 1729 is known as the Hardy-Ramanujan number. It’s the smallest number expressible as the sum of two cubes in two different ways: 1729 = 1^3 + 12^3 = 9^3 + 10^3.",
    "A perfect number is a positive integer that is equal to the sum of its proper divisors (excluding itself). Example: 28 (1 + 2 + 4 + 7 + 14 = 28).",
    "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. Example: 7.",
    "There are infinitely many prime numbers, a fact proven by the ancient Greek mathematician Euclid.",
    "The number e (Euler's Number) is an irrational number approximately equal to 2.71828. It is the base of natural logarithms.",
    "Pythagorean triples are sets of three positive integers a, b, and c that fit the formula a^2 + b^2 = c^2. Example: (3, 4, 5).",
    "The Golden Ratio, often denoted by the Greek letter φ (phi), is approximately equal to 1.618 and appears in various forms in art, architecture, and nature.",
    "A Mobius strip is a surface with only one side and one boundary curve.",
    "The Four Color Theorem states that no more than four colors are needed to color the regions of any map in such a way that no two adjacent regions have the same color.",
    "In base 10, a number is divisible by 3 if the sum of its digits is divisible by 3.",
    "Magic squares are square arrays of numbers where the sums of the numbers in each row, column, and diagonal are the same. Example: a 3x3 magic square where each row, column, and diagonal sums to 15.",
    "The square root of 2 is an irrational number; it cannot be expressed as a simple fraction.",
    "The concept of zero as a number was first developed in India by mathematician Brahmagupta in the 7th century.",
    "A Mersenne prime is a prime number that is one less than a power of two. Example: 2^5 - 1 = 31."
]

people = {
"Contributed to the development of algebraic topology and homotopy theory":"Jean-Pierre Serre",
"Contributed to the development of modern calculus and analysis":"Augustin-Louis Cauchy",
"Contributed to the field of numerical analysis and approximation theory":"Carl Gustav Jacobi",
"Developed the axiomatic system for Euclidean geometry":"Euclid",
"Developed the calculus independently along with Isaac Newton":"Gottfried Wilhelm Leibniz",
"Developed the concept of Hilbert space in functional analysis":"John von Neumann",
"Developed the concept of a Turing machine and formalized the notion of computation":"Alan Turing",
"Developed the field of game theory and contributed to economic theory":"John Nash",
"Developed the foundation of modern probability theory":"Andrey Kolmogorov",
"Developed the fundamental theorem of calculus":"James Gregory",
"Developed the modern formulation of algebraic geometry":"David Hilbert",
"Developed the modern theory of modular forms and elliptic curves":"Srinivasa Ramanujan",
"Developed the proof of Fermat's Last Theorem":"Andrew Wiles",
"Developed the proof of the Poincaré conjecture in topology":"Grigori Perelman",
"Developed the theory of relativity and contributed to quantum mechanics":"Albert Einstein",
"Formulated the laws of motion and universal gravitation":"Isaac Newton",
"Introduced the Cartesian coordinate system and made contributions to philosophy":"René Descartes",
"Introduced the concept of complex numbers and made contributions to analysis":"Carl Friedrich Gauss",
"Known for her work on the foundations of mathematics and the concept of formal systems":"Bertrand Russell",
"Known for his contributions to algebra and the theory of fields":"Évariste Galois",
"Known for his contributions to number theory and his namesake last theorem":"Pierre de Fermat",
"Known for his incompleteness theorems in mathematical logic":"Kurt Gödel",
"Known for his work in algebraic geometry and the Weil conjectures":"André Weil",
"Known for his work in combinatorics, graph theory, and probability":"Paul Erdős",
"Known for his work in differential equations and mathematical physics":"Joseph Fourier",
"Known for his work in linear programming and operations research":"George Dantzig",
"Known for his work on fractals and chaos theory":"Benoît B. Mandelbrot",
"Known for his work on functional analysis and measure theory":"Émile Borel",
"Known for his work on the distribution of prime numbers and the Riemann Hypothesis":"Bernhard Riemann",
"Known for the formulation of Boolean algebra and symbolic logic":"George Boole",
"Made foundational contributions to the field of computer science and cryptography":"Alan Turing",
"Made significant contributions to algebraic topology":"Henri Poincaré",
"Made significant contributions to the field of mathematical logic":"Alfred Tarski",
"Made significant contributions to topology and abstract algebra":"Emmy Noether",
"Pioneered the field of category theory":"Saunders Mac Lane",
"Pioneered the field of set theory and introduced the concept of cardinality":"Georg Cantor",
"Pioneered the use of algorithms and data structures in computer science":"Donald Knuth"
    }

options = [
    'Usage Guide📃',
    'Games🎮',
    'Random fact🎁',
    'Chat🗨️',
    'Close current session👋']
