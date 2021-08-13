from sage.all import *
import sys

# Classifies isogeny classes of Elliptic curves of j-invariant 0 or 1728 over finite fields.
# For each field GF(p^EXP) where LOWER_LIMIT <= p <= UPPER_LIMIT, this program outputs all
# isogeny classes of elliptic curves with J_INVARIANT 0 or 1728.
#
# The output format is split into blocks, one block per field. At the top of the block is
# a designation of which finite field the below pertains to, for example, q=5. Within each
# block, each line is a list of isogenous curves. Each curve is represented as a pair (B,S)
# where B is a paramter identifying the curve and S is a representation of  the curve's
# abelian group.

# For example, if J_INVARIANT = 0, then the B parameter is the constant term in the curve's
# definition (so a curve with B=6 has formula y^2 = x^3 + 6). Likewise, if J_INVARIANT = 1728
# then a curve with B=6 has formula y^2 = x^3 + 6x.

# parameters
lower_limit = 5
upper_limit = 12
exp = 1 # exponent to raise to
j_invariant = 0 # can be either 0 or 1728.

#takes the abelian_group, G, of an Elliptic Curve
#and returns string which represents the canonical
#isomorphic group.
def getGroupStructure(G):
    words = str.split(str(G)," ")
    if(words[6] != '+'):
        return words[5]
    return (words[5]+words[6]+words[7])

#wrapper for getGroupStructure. Returns '(b, s)'
#where 's' is group structure of curve y^2=x^3+b over Z_p
def getCurveInfo(b,p, E):
    s = getGroupStructure(E.abelian_group())
    return ("({}, {})".format(b, s))

def getCurve(b, p, j):
    if j == 0:
        return EllipticCurve(GF(p), [0,b])
    elif j == 1728:
        return EllipticCurve(GF(p), [b,0])
    else:
        sys.exit('Invalid value for j_invariant. Only 0 or 1728 is allowed.')

f = open("p^" + str(exp) + "-" + str(j_invariant) + "_invariant.dat","w+")

primes = prime_range(lower_limit, upper_limit)
for p in primes:
    p = p**exp
    f.write("q = %d\n" % p)

    # Since curves have j invariant 0 or 1728, they can be easily parameterized.
    B = list(GF(p))
    for b in list(GF(p)):
        # If the curve would be singular, throw it away.
        if((j_invariant == 0 and (27*b**2) == 0 or
            (j_invariant == 1728 and b**3 == 0))):
            B.remove(b)
    B2 = B[:]


    # find isogeny classes (not efficient)
    for b in B2:
        if(b in B):
            E1 = getCurve(b, p, j_invariant)
            for b2 in B2:
                if(b2 in B):
                    E2 = getCurve(b2, p, j_invariant)
                    if(E1.is_isogenous(E2)):
                        f.write("%s, " % getCurveInfo(b2,p, E2))
                        B.remove(b2)
            f.write("\n")
    f.write("\n\n")

f.close()
