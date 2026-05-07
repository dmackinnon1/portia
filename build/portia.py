"""
Portia Casket Puzzle Generator
================================
Generates logic puzzles inspired by the casket riddle in Shakespeare's
Merchant of Venice, where a suitor must deduce which casket holds a
portrait based on statements inscribed on the caskets.

PUZZLE FRAMEWORK
----------------
There are n caskets (typically 3). One contains a portrait. Each casket
bears one or more statements. The puzzle-setter knows where the portrait
is and announces a clue derived from that knowledge. The solver uses the
clue and the visible statements to deduce the portrait's location.

STATEMENT TYPES (Pointers)
---------------------------
Each statement is encoded as a signed integer called a "pointer":
  +k  means "the portrait IS in casket k"
  -k  means "the portrait is NOT in casket k"

A statement is true or false depending on where the portrait actually is.
The function truthAtPointer(p, pointer) evaluates this for a given
portrait position p.

THREE PUZZLE VARIANTS
---------------------
Portia I   — One statement per casket. The clue is the total number of
             true statements across all caskets, which uniquely identifies
             the portrait's location. See: checkForPortia1, json.

Portia II  — Two statements per casket (from two independent pointer
             sequences). The clue is a per-casket truth count vector,
             which must be distinct from all other possible vectors.
             See: checkForPortia2, json2.

Portia III — One statement per casket, but statements are arranged in a
             Bellini/Cellini cyclic topology (each casket's statement
             references the next casket in a deranged cycle). One
             statement in the cycle is negated (antipathy/sympathy).
             See: checkForPortia3, json3.

OUTPUT FORMAT AND PRESENTATION LAYER
--------------------------------------
Each generator writes a JSON array to a file. The presentation layer
(e.g. a web app or game) reads these files to display puzzles.

Portia I JSON entry fields:
  "caskets"   — list of n pointers, one per casket. The presentation
                layer renders each as a natural-language statement:
                +k → "The portrait is in casket k"
                -k → "The portrait is not in casket k"
  "truths"    — the total number of true statements when the portrait
                is in the solution casket. This is the clue given to
                the solver.
  "solution"  — the casket number (1-indexed) that holds the portrait.
  "position"  — "min", "mid", or "max", indicating where "truths" falls
                relative to the truth counts for other portrait positions.
                This tells the presentation layer which clue phrasings
                are available:
                  "min" → can say "at most N statements are true" OR
                          "exactly N statements are true"
                  "max" → can say "at least N statements are true" OR
                          "exactly N statements are true"
                  "mid" → can only say "exactly N statements are true"
                The threshold forms ("at least", "at most") make harder
                puzzles because the solver must work out that no position
                exceeds or falls below the threshold, rather than simply
                matching an exact count.
  "id"        — unique identifier string, e.g. "portia1-42"

Portia II JSON entry fields:
  "caskets"   — list of two pointer sequences [seq1, seq2]. The i-th
                casket bears statement seq1[i] and statement seq2[i].
  "truths"    — a list of per-casket truth counts for the solution
                position, e.g. [2, 1, 0] means casket 1 has 2 true
                statements, casket 2 has 1, casket 3 has 0.
  "solution"  — the solution casket number (1-indexed).
  "id"        — unique identifier string, e.g. "portia2-7"

Portia III JSON entry fields:
  "caskets"   — a list [pointers, belliniSeq] where pointers is the
                primary statement sequence and belliniSeq is the
                Bellini/Cellini secondary sequence (one element negated).
  "truths"    — a list of per-statement truth values (0 or 1) for the
                solution position, one per casket.
  "solution"  — the solution casket number (1-indexed).
  "id"        — unique identifier string, e.g. "portia3-3"
"""


# ---------------------------------------------------------------------------
# Core statement evaluation
# ---------------------------------------------------------------------------

def casketPointers(n):
    """
    Return the full set of possible statement pointers for n caskets.

    Produces [1, 2, ..., n, -1, -2, ..., -n]. Each positive value k
    represents the statement "the portrait is in casket k", and each
    negative value -k represents "the portrait is NOT in casket k".

    Used as the pool of possible statements when generating all puzzle
    configurations for Portia I, II, and III.
    """
    return [i+1 for i in range(n)] + [-1*(i+1) for i in range(n)]


def caskets(n):
    """
    Return the list of casket labels [1, 2, ..., n].

    Used throughout as a convenient 1-indexed range for iterating over
    casket positions.
    """
    return [i+1 for i in range(n)]


def truthAtPointer(p, pointer):
    """
    Evaluate whether a single statement (pointer) is true given that
    the portrait is at position p.

    Parameters
    ----------
    p       : int — the casket number (1-indexed) containing the portrait
    pointer : int — the statement to evaluate:
                    positive k  → "portrait IS in casket k"
                    negative -k → "portrait is NOT in casket k"

    Returns 1 if the statement is true, 0 if false.

    Truth rules:
      +k is true iff p == k   (portrait is exactly where stated)
      -k is true iff p != k   (portrait is anywhere except casket k)
    """
    if p == pointer:
        return 1
    if pointer < 0:
        if p != -1 * pointer:
            return 1
    return 0


# ---------------------------------------------------------------------------
# Portia I — truth sequence (global true-statement count per position)
# ---------------------------------------------------------------------------

def initialTruthSequence(n):
    """
    Return a zero-initialised truth sequence of length n.

    Used as the accumulator in truthForPointers before counting begins.
    """
    return [0 for i in range(n)]


def truthForPointers(pointerSequence):
    """
    Compute the truth sequence for a Portia I configuration.

    For each possible portrait position i (1..n), counts the total number
    of statements in pointerSequence that would be true if the portrait
    were in casket i. Returns a list of n such totals.

    Example — pointers [1, 2, -3] with n=3:
      If portrait in casket 1: stmt +1 true, +2 false, -3 true  → total 2
      If portrait in casket 2: stmt +1 false, +2 true, -3 true  → total 2
      If portrait in casket 3: stmt +1 false, +2 false, -3 false → total 0
      Truth sequence: [2, 2, 0]

    This total — not any individual casket's count — is the clue
    announced to the solver in a Portia I puzzle.
    """
    n = len(pointerSequence)
    c = caskets(n)
    truthSeq = initialTruthSequence(n)
    for i in c:
        for j in pointerSequence:
            truthSeq[i-1] += truthAtPointer(i, j)
    return truthSeq


def matches(t, sequence):
    """
    Return a list of 1s, one for each element in sequence that equals t.

    The length of the returned list is the count of occurrences of t.
    Used by isDistinct.
    """
    return [1 for i in sequence if i == t]


def isDistinct(t, sequence):
    """
    Return True if the value t appears exactly once in sequence.

    A truth count is 'distinct' if no other portrait position produces
    the same count — meaning it can uniquely identify a solution.
    """
    return len(matches(t, sequence)) == 1


def whichDistinct(truthSequence):
    """
    Return a list of 1-indexed positions whose truth count is unique
    within the truth sequence.

    These are the only positions that can serve as valid Portia I puzzle
    solutions: a position is solvable iff its total true-statement count
    is shared by no other position, allowing the solver to identify it
    from the announced count alone.

    Example — truthSequence [2, 2, 0]: only position 3 is distinct,
    so only casket 3 is a valid solution for this configuration.
    """
    indexes = range(len(truthSequence))
    return [i+1 for i in indexes if isDistinct(truthSequence[i], truthSequence)]


def positionalTruth(c, t):
    """
    Classify a truth count c relative to the full truth sequence t.

    Returns "min", "max", or "mid" depending on whether c is the
    smallest, largest, or intermediate value in t.

    This classification determines which clue phrasings the presentation
    layer can offer to the solver:

      "max" → the exact clue "there are N true statements" can be
              rephrased as the harder "there are AT LEAST N true
              statements." The solver must deduce that no position
              yields more than N to narrow it down.

      "min" → the exact clue can be rephrased as the harder "there are
              AT MOST N true statements." The solver must deduce that
              no position yields fewer than N.

      "mid" → only the exact form "there are N true statements" is
              available, since a threshold clue would not isolate
              a middle value.

    The threshold phrasings make harder puzzles: the solver must reason
    about bounds rather than simply matching an exact count.
    """
    if c == min(t): return "min"
    if c == max(t): return "max"
    return "mid"


def checkForPortia1(pointers):
    """
    Find all valid Portia I puzzle solutions for a given pointer sequence.

    Computes the truth sequence, then returns one puzzle definition for
    each portrait position that has a unique truth count. Returns an
    empty list if no position has a unique count (puzzle unsolvable).

    Each returned entry is: [pointers, truthCount, solutionCasket, position]
      pointers     — the input pointer sequence (the casket statements)
      truthCount   — total true statements when portrait is at solution
      solutionCasket — 1-indexed casket number of the solution
      position     — "min", "max", or "mid" (see positionalTruth)

    A single pointer sequence can yield up to n puzzle entries (one per
    distinct truth count), each with a different solution casket and clue.
    """
    t = truthForPointers(pointers)
    return [[pointers, t[i-1], i, positionalTruth(t[i-1], t)] for i in whichDistinct(t)]


# ---------------------------------------------------------------------------
# Portia II — per-casket truth distribution
# ---------------------------------------------------------------------------

def truthForPointers2(pointerSequence1, pointerSequence2):
    """
    Compute per-casket truth counts for a Portia II configuration.

    In Portia II each casket bears two statements: one from each of the
    two pointer sequences. For each possible portrait position i, this
    function computes how many of each casket's two statements are true.

    Returns a list of n sub-lists. The sub-list at index i-1 contains n
    values (one per casket), each being 0, 1, or 2: the count of true
    statements on that casket if the portrait is in casket i.

    Example with n=3, seq1=[1,2,3], seq2=[-2,-3,-1]:
      If portrait in casket 1:
        casket 1: +1 true, -2 true  → 2
        casket 2: +2 false, -3 true → 1
        casket 3: +3 false, -1 true → 1
      → sub-list for position 1: [2, 1, 1]

    The clue given to the solver is the sub-list for the actual solution
    position, e.g. "casket 1 has 2 true statements, casket 2 has 1, ..."
    """
    n = len(pointerSequence1)
    c = caskets(n)
    truthVector = []
    for i in c:
        truthAti = []
        for j in range(n):
            truthCount = truthAtPointer(i, pointerSequence1[j])
            truthCount += truthAtPointer(i, pointerSequence2[j])
            truthAti.append(truthCount)
        truthVector.append(truthAti)
    return truthVector


def isPermutation(v1, v2):
    """
    Return True if v1 and v2 contain the same elements with the same
    multiplicities (i.e. are permutations of each other).

    Uses sorted comparison to correctly handle duplicate values.
    For example, [2, 0, 1] and [1, 2, 0] are permutations; [2, 2, 0]
    and [2, 1, 0] are not.

    NOTE: An earlier version of this function incorrectly checked only
    whether each element of v1 appeared somewhere in v2, without
    accounting for duplicates. That version could falsely identify
    [2, 2, 0] as a permutation of [2, 1, 0]. The sorted() comparison
    here is correct.
    """
    return sorted(v1) == sorted(v2)


def noPermutationInList(d, lst):
    """
    Return True if no element of lst is a permutation of d.

    Used in Portia II to ensure the truth distribution for the solution
    position is not rearrangeable into the distribution of any other
    position. If two positions share the same multiset of per-casket
    truth counts, the solver cannot distinguish them from the clue alone,
    so the puzzle would be unsolvable.
    """
    for c in lst:
        if isPermutation(d, c):
            return False
    return True


def checkForPortia2(casketTuple):
    """
    Find all valid Portia II puzzle solutions for a given pair of pointer
    sequences.

    Parameters
    ----------
    casketTuple : (list, list) — a pair (seq1, seq2) of pointer sequences
                  of equal length n. Each casket i bears the statement
                  seq1[i] and seq2[i].

    For each portrait position i, checks whether the per-casket truth
    distribution is distinct from all other positions' distributions (up
    to permutation). Returns one puzzle entry per valid position.

    Each returned entry is: [casketTuple, truthDistribution, solutionCasket]
      casketTuple       — the input pair of pointer sequences
      truthDistribution — per-casket truth count list for the solution
      solutionCasket    — 1-indexed solution casket number

    The presentation layer displays the two statements on each casket and
    announces the per-casket truth counts as the clue. The solver reasons:
    "which portrait position would produce this exact distribution?"
    """
    casketSet1 = casketTuple[0]
    casketSet2 = casketTuple[1]
    solutionList = []
    t = truthForPointers2(casketSet1, casketSet2)
    for i in range(len(t)):
        remaining = list(t)
        remaining.remove(t[i])
        if noPermutationInList(t[i], remaining):
            solutionList.append(i)
    return [[casketTuple, t[i], i+1] for i in solutionList]


# ---------------------------------------------------------------------------
# Portia III — Bellini/Cellini cyclic statement topology
# ---------------------------------------------------------------------------

def truthSequence(p, pointers):
    """
    Return a per-statement truth value list for portrait position p.

    Unlike truthForPointers (which sums across all statements), this
    returns the individual truth value of each statement in pointers
    when the portrait is at position p. Used in Portia III where the
    solver reasons about which individual statements are true or false.

    Returns a list of 0s and 1s, one per pointer.
    """
    return [truthAtPointer(p, i) for i in pointers]


def belliniCellini1(n):
    """
    Generate all deranged cyclic permutations of [1, 2, ..., n].

    A deranged cycle is a permutation of [1..n] such that:
      - no element remains in its original position (derangement), and
      - the permutation forms a single cycle of length n.

    For n=3 this yields [[2, 3, 1], [3, 1, 2]] — the two non-trivial
    rotations.

    In Portia III, these cycles define the topology of the secondary
    (Bellini/Cellini) statements. Each casket i's secondary statement
    references casket cycle[i-1]. This creates a chain where each casket
    comments on the next one in the cycle, with no casket commenting on
    itself. One element of the cycle is then negated (see
    negateOnePerSequence) to introduce a single sympathy/antipathy
    statement among otherwise accusation/affirmation statements.
    """
    c = caskets(n)
    result = []
    cp = c[1:len(c)]  # start partial sequences from casket 2..n (never 1,
    # since element 1 cannot occupy position 1 in a derangement)
    for j in cp:
        result.append([j])
    for i in cp:
        remainders = c[:]
        newResult = []
        for k in result:
            # remainderk: elements not yet used in this partial sequence,
            # excluding the current 'forbidden' element i
            remainderk = removeAll(remainders, k)
            remainderk = removeIfPresent(remainderk, i)
            if len(remainderk) == 0:
                # no valid extension available; carry sequence forward as-is
                # (it will be filtered out at the end if too short)
                newResult.append(k)
            for r in remainderk:
                p = k[:]
                p.append(r)
                newResult.append(p)
        result = newResult[:]
    # keep only complete sequences of length n
    return [i for i in result if len(i) == n]


def negateOnePerSequence(sequences):
    """
    For each sequence in sequences, produce n variants, one for each
    position. In variant i, element i is replaced by its negation (-1 * element).

    Used in Portia III to introduce exactly one sympathy/antipathy
    statement into each otherwise all-accusation/affirmation Bellini/
    Cellini cycle. The negated element's casket bears a statement of the
    form "portrait is NOT in casket k" rather than "portrait IS in casket k".

    Returns a flat list of all variants across all input sequences.
    """
    return [negateInSequence(i, s) for s in sequences for i in range(len(s))]


def negateInSequence(i, s):
    """
    Return a copy of sequence s with element at index i negated.
    """
    r = s[:]
    r[i] = -1 * r[i]
    return r


def hasPointer(i, pointers):
    """
    Return True if portrait position i is determinable from the given
    pointer list, according to Portia III requirements.

    A position i is considered determinable if any of the following hold:
      1. A positive pointer +i exists (the solution casket is directly named)
      2. A negative pointer -i exists (i is explicitly ruled out — note this
         statement is false when the portrait IS at i, so its falsity
         contributes to the reasoning)
      3. The pointers reference more than one distinct casket (len(set of
         abs values) > 1), allowing indirect elimination

    Used to filter which portrait positions can yield solvable Portia III
    puzzles for a given set of primary pointers.
    """
    for j in pointers:
        if i == j:  return True   # i directly named as solution
        if i == -1 * j: return True  # i referenced in a negative statement
    a = [abs(j) for j in pointers]
    if len(set(a)) > 1: return True  # pointers span multiple caskets
    return False


def pointerList(pointers):
    """
    Return all portrait positions (1..n) for which a valid Portia III
    puzzle can be constructed using the given pointer sequence.

    Filters casket positions using hasPointer to find those where the
    portrait location is determinable given the statement topology.
    """
    n = len(pointers)
    c = caskets(n)
    return [i for i in c if hasPointer(i, pointers)]


def checkForPortia3(pointers):
    """
    Find all valid Portia III puzzle definitions for a given primary
    pointer sequence.

    For each valid portrait position (from pointerList), and for each
    Bellini/Cellini secondary sequence (from belliniCellini1 with one
    element negated), produces a puzzle definition.

    Each returned entry is: [[pointers, belliniSeq], truthValues, solutionCasket]
      pointers      — the primary statement sequence (one per casket)
      belliniSeq    — the secondary Bellini/Cellini sequence (one per casket,
                      with exactly one element negated)
      truthValues   — list of per-statement truth values (0 or 1) for the
                      solution position
      solutionCasket — 1-indexed solution casket number

    The presentation layer displays both the primary and secondary statements
    on each casket and uses the truth values to construct the puzzle clue.
    """
    l = pointerList(pointers)
    if len(l) == 0:
        return []
    return [[[pointers, j], truthSequence(i, pointers), i]
            for i in l
            for j in negateOnePerSequence(belliniCellini1(len(pointers)))]


# ---------------------------------------------------------------------------
# JSON output formatters
# ---------------------------------------------------------------------------

def json(puzzleDef, counter):
    """
    Format a Portia I puzzle definition as a JSON object string.

    Parameters
    ----------
    puzzleDef : [pointers, truthCount, solutionCasket, position]
                As returned by checkForPortia1.
    counter   : int — sequential puzzle number for the id field.

    Output fields (see module docstring for full field descriptions):
      "caskets"  — pointer list, e.g. [1, 2, -3]
      "truths"   — total true statements at solution, e.g. 0
      "solution" — solution casket number, e.g. 3
      "position" — "min", "mid", or "max"
      "id"       — e.g. "portia1-42"

    Presentation layer usage:
      - Render each pointer as a statement string on the corresponding casket.
      - Use "truths" and "position" together to choose the clue phrasing:
          "mid"  → "Exactly {truths} of the statements are true."
          "max"  → "Exactly {truths} ..." or harder:
                   "At least {truths} of the statements are true."
          "min"  → "Exactly {truths} ..." or harder:
                   "At most {truths} of the statements are true."
      - "solution" is the answer; keep hidden until the solver submits.
    """
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": "   + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"position\": \"" + puzzleDef[3] + "\""
    result += ", \"id\": "       + "\"portia1-" + str(counter) + "\"}"
    return result


def json2(puzzleDef, counter):
    """
    Format a Portia II puzzle definition as a JSON object string.

    Parameters
    ----------
    puzzleDef : [casketTuple, truthDistribution, solutionCasket]
                As returned by checkForPortia2.
    counter   : int — sequential puzzle number for the id field.

    Output fields (see module docstring for full field descriptions):
      "caskets"  — list of two pointer sequences, e.g. [[1,2,3],[-2,-3,-1]]
      "truths"   — per-casket truth count list, e.g. [2, 1, 0]
      "solution" — solution casket number
      "id"       — e.g. "portia2-7"

    Presentation layer usage:
      - Each casket i displays statement seq1[i] and statement seq2[i].
      - The clue announces the truth count for each casket:
        "Casket 1 has 2 true statements, casket 2 has 1, casket 3 has 0."
      - The solver determines which portrait position produces that
        exact per-casket distribution.
    """
    result  = "{\"caskets\": ["
    result += str(puzzleDef[0][0])
    result += ", "
    result += str(puzzleDef[0][1])
    result += "], \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"id\": " + "\"portia2-" + str(counter) + "\"}"
    return result


def json3(puzzleDef, counter):
    """
    Format a Portia III puzzle definition as a JSON object string.

    Parameters
    ----------
    puzzleDef : [[pointers, belliniSeq], truthValues, solutionCasket]
                As returned by checkForPortia3.
    counter   : int — sequential puzzle number for the id field.

    Output fields (see module docstring for full field descriptions):
      "caskets"  — [primaryPointers, belliniSeq], e.g. [[1,-2,3],[2,3,-1]]
      "truths"   — per-statement truth values for solution, e.g. [1,0,1]
      "solution" — solution casket number
      "id"       — e.g. "portia3-3"

    Presentation layer usage:
      - Each casket i displays its primary statement (pointers[i]) and
        its secondary Bellini/Cellini statement (belliniSeq[i]).
      - The clue uses the truth values to tell the solver which statements
        are true and which are false (or a count thereof).
      - The solver uses the pattern of true/false values alongside the
        cyclic statement structure to deduce the portrait's location.
    """
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"id\": " + "\"portia3-" + str(counter) + "\"}"
    return result


# ---------------------------------------------------------------------------
# Sequence generation utilities
# ---------------------------------------------------------------------------

def allSequences(n, elements):
    """
    Recursively generate all ordered sequences of length n drawn from
    elements (with repetition allowed).

    Returns a list of lists. For n=2, elements=[1,2]: [[1,1],[1,2],[2,1],[2,2]].
    Used to enumerate all possible pointer assignments across n caskets.

    Note: returns [] for n=0 (the n=1 base case is reached before n=0
    in all practical uses of this function).
    """
    if n == 0:
        return []
    if n == 1:
        return [[i] for i in elements]
    return appendTo(elements, allSequences(n-1, elements))


def appendTo(elements, listOfLists):
    """
    Extend each list in listOfLists by appending each element of elements,
    returning all resulting combinations.

    Helper for allSequences.
    """
    return [copyAppend(l, i) for l in listOfLists for i in elements]


def copyAppend(l, i):
    """
    Return a new list equal to l with i appended.

    Creates a copy to avoid mutating the input list.
    """
    n = list(l)
    n.append(i)
    return n


def allNoMatchSequencePairs(n, elements):
    """
    Generate all ordered pairs of sequences (s, t) of length n from
    elements such that s[i] != t[i] for every position i.

    Used in Portia II to ensure the two statement sequences on each casket
    are never identical at the same casket position — i.e. no casket bears
    the same statement twice.

    Iterates over all pairs without repetition (each unordered pair
    appears once) and filters by the noMatch condition.
    """
    pairs = []
    sequences = allSequences(n, elements)
    decreasing = list(sequences)
    for s in sequences:
        decreasing.remove(s)
        for t in decreasing:
            if noMatch(s, t):
                pairs.append((s, t))
    return pairs


def noMatch(l1, l2):
    """
    Return True if l1 and l2 differ at every position (no shared value
    at any index).

    Used to ensure the two pointer sequences in a Portia II configuration
    never assign the same statement to the same casket.
    """
    for i in range(len(l1)):
        if l1[i] == l2[i]:
            return False
    return True


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def removeAll(p, d):
    """
    Return a copy of list p with every element of list d removed
    (each removed at most once, in order).

    Used in belliniCellini1 to track which casket numbers remain
    available when building partial deranged cycle sequences.
    """
    q = p[:]
    for i in d:
        removeIfPresent(q, i)
    return q


def removeIfPresent(p, i):
    """
    Remove element i from list p in place if it is present.
    Returns p (modified in place).
    """
    if i in p:
        p.remove(i)
    return p


# ---------------------------------------------------------------------------
# Top-level puzzle generators
# ---------------------------------------------------------------------------

def generateAllPuzzlesPortia1(n):
    """
    Generate all valid Portia I puzzles for n caskets and return as a
    JSON array string.

    Iterates over all (2n)^n possible pointer assignments (one pointer
    per casket), checks each for solvability, and collects valid puzzle
    definitions. Prints the total number of puzzles generated.

    For n=3 the pool is 6 pointers and 6^3 = 216 configurations are
    checked, typically yielding several hundred valid puzzles.
    """
    cp = casketPointers(n)
    allPossible = allSequences(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia1(i)
        for j in results:
            if not first:
                result += ",\n"
            first = False
            result += "\t"
            counter += 1
            result += json(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result


def generateAllPuzzlesPortia2(n):
    """
    Generate all valid Portia II puzzles for n caskets and return as a
    JSON array string.

    Iterates over all pairs of non-positionally-matching pointer sequences
    (ensuring no casket bears the same statement twice), checks each pair
    for solvability, and collects valid puzzle definitions.
    """
    cp = casketPointers(n)
    allPossible = allNoMatchSequencePairs(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia2(i)
        for j in results:
            if not first:
                result += ",\n"
            first = False
            result += "\t"
            counter += 1
            result += json2(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result


def generateAllPuzzlesPortia3(n):
    """
    Generate all valid Portia III puzzles for n caskets and return as a
    JSON array string.

    Iterates over all pointer assignments as primary statements, then for
    each generates all Bellini/Cellini secondary statement topologies
    (deranged cycles with one negated element). Checks each combination
    for solvability and collects valid puzzle definitions.
    """
    cp = casketPointers(n)
    allPossible = allSequences(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia3(i)
        for j in results:
            if not first:
                result += ",\n"
            first = False
            result += "\t"
            counter += 1
            result += json3(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result


# ---------------------------------------------------------------------------
# Puzzle Generator — entry point
# ---------------------------------------------------------------------------

print('-------------------------------------------')
print('Generating Portia I data.')
print(' --- creating file ../data/portia1.json')
f = open("../data/portia1.json", "w")
f.write(generateAllPuzzlesPortia1(3))
f.close()
print(' --- completed writing out Portia I data.')
print('-------------------------------------------')
print("Generating Portia II data.")
print(' --- creating file ../data/portia2.json')
f = open("../data/portia2.json", "w")
f.write(generateAllPuzzlesPortia2(3))
f.close()
print(' --- completed writing out Portia II data.')
print('-------------------------------------------')
print("Generating Portia III data.")
print(' --- creating file ../data/portia3.json')
f = open("../data/portia3.json", "w")
f.write(generateAllPuzzlesPortia3(3))
f.close()
print(' --- completed writing out Portia III data.')
print('-------------------------------------------')
