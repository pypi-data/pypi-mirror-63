import numpy as numpy
from threading import Thread

from .Engine import Engine
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  *
#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2020 Do Kester


threadErrors = []

class Explorer( object ):
    """
    Explorer is a helper class of NestedSampler, which contains and runs the
    diffusion engines.

    It uses Threads to parallelise the diffusion engines.

    Attributes
    ----------
    walkers : WalkerList
        walkers to be explored
    engines : [engine]
        list of engines to be used
    errdis : ErrorDistribution
        to be used
    rng : numpy.random.RandomState
        random number generator
    rate : float (1.0)
        governs processing speed (vs precision)
    maxtrials : int (5)
        number of trials
    verbose : int (0)
        level of blabbering
    lowLhood : float
        present low likelihood level
    iteration : int
        counting explorer calls

    Author       Do Kester.

    """
    TWOP32 = 2 ** 32

    def __init__( self, ns, threads=False ):
        """
        Construct Explorer from a NestedSampler object.

        Parameters
        ----------
        ns : NestedSampler
            the calling NestedSampler. It provides the attributes.

        """
        self.walkers = ns.walkers
        self.engines = ns.engines
        self.errdis = ns.distribution
        self.rng = ns.rng
        self.rate = ns.rate
        self.maxtrials = ns.maxtrials
        self.verbose = ns.verbose
        self.threads = threads
        self.iteration = ns.iteration

    def explore( self, worst, lowLhood ):
        """
        Explore the likelihood function, using threads.

        Parameters
        ----------
        worst : [int]
            list of walkers to be explored/updated
        lowLhood : float
            level of the low likelihood

        """
        if not self.threads :
            for kw in worst :
                walker = self.walkers[kw]
                self.exploreWalker( walker, lowLhood, self.engines, self.rng )
            return

        ## We have Threads
        explorerThreads = []
        self.lowLhood = lowLhood

        nrep = Engine.NCALLS
        for kw in worst :
            seed = self.rng.randint( self.TWOP32 )
            walker = self.walkers[kw]
#            print( "Thr  %d  "%kw, seed )
            exThread = ExplorerThread( "explorer_%d"%kw, walker, self, seed )
            exThread.start( )
            explorerThreads += [exThread]

        for thread in explorerThreads :
            thread.join( )

            for k,engine in enumerate( self.engines ) :
                nc = 0
                for i in range( nrep ) :
                    nc += thread.engines[k].report[i]
                    engine.report[i] += thread.engines[k].report[i]
                engine.report[nrep] += nc

        if len( threadErrors ) > 0: #check if there are any errors
            for e in threadErrors:
                print( e )
            raise Exception( "Thread Error" )

    def exploreWalker( self, walker, lowLhood, engines, rng ):
        """ For internal use only """

        oldlogL = walker.logL

        maxmoves = len( walker.fitIndex ) / self.rate
        maxtrials = self.maxtrials / self.rate

        moves = 0
        trials = 0


        while moves < maxmoves and trials < maxtrials :
            i = 0
            for engine in rng.permutation( engines ) :

                moves += engine.execute( walker, lowLhood )

                if self.verbose >= 4:
                    print( "%4d %-15.15s %4d %10.3f %10.3f ==> %3d  %10.3f"%
                            ( trials, engine, walker.id, lowLhood, oldlogL, moves,
                                walker.logL ) )
                    if len( walker.allpars ) < len( walker.fitIndex ) :
                        raise ValueError( "Walker parameter %d fitIndex %d" %
                            ( len( walker.allpars ), len( walker.fitIndex ) ) )
                    i += 1
                    oldlogL = walker.logL

            trials += 1

        if moves == 0 :
            self.logLcheck( walker )

        return

    def logLcheck( self, walker ) :
        """
        Sanity check when no moves are found, if the LogL is still the same as the stored logL.

        Parameters
        ----------
        walker : Walker
            the one with the stored logL

        Raises
        ------
        ValueError at inconsistency.

        """
        wlogL = self.errdis.logLikelihood( walker.problem, walker.allpars )
        if wlogL != walker.logL :
            print( "Iteration %4d %4d %10.3f  %10.3f" % (self.iteration, walker.id, walker.logL, wlogL ) )
            print( fmt( walker.allpars, max=None, format="%3d" ) )
            raise ValueError( "Inconsistency between stored logL %f and calculated logL %f" %
                                ( walker.logL, wlogL ) )


class ExplorerThread( Thread ):
    """
    One thread for the Explorer. It updates one walker.

    Attributes
    ----------
    id : int
        identity for thread
    walkers : WalkerList
        list of walkers
    rng : numpy.random.RandomState
        random number generator
    engines : [Engine]
        copy of the list of Engines of Explorer
    """

    global threadErrors

    def __init__( self, name, walker, explorer, seed ):
        super( ExplorerThread, self ).__init__( name=name )
        self.walker = walker
        self.explorer = explorer
        self.engines = [eng.copy() for eng in explorer.engines]
        self.rng = numpy.random.RandomState( seed )


    def run( self ):
        try :
            self.explorer.exploreWalker( self.walker, self.explorer.lowLhood,
                                         self.engines, self.rng )
        except Exception as e :
            threadErrors.append( [repr(e) + " occurred in walker %d" % self.walker.id] )
            raise



