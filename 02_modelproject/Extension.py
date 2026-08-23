import numpy as np
from Government import GovernmentClass

class PigouvianGovernmentClass(GovernmentClass):
    """ extends GovernmentClass with a per-unit externality on bus travel (with the possibility of adding to other goods)

    Consuming good 2 causes an external cost of c2 per unit (e.g. congestion,
    emissions) that the consumer's own utility does not see. Social welfare is private
    utility net of this cost: W = u - c2*x2.

    The revenue-maximizing tax rate from GovernmentClass.max_revenue() ignores this
    cost entirely, since revenue leaves the model. The welfare-maximizing rate found
    here is the corrective (Pigouvian) tax instead.
    """

    def setup_government(self):
        super().setup_government()
        par = self.par
        par.c1 = 0.0 # external cost per unit of food (none, by default)
        par.c2 = 0.0 # external cost per bus trip
        par.c3 = 0.0 # external cost per train trip

    def externality_cost(self,opt=None):
        """ total external cost of the consumer's chosen bundle """

        par = self.par

        # a. what does the consumer buy
        if opt is None: opt = self.solve(do_print=False)
        x1,x2,x3 = self.quantities(opt.s1,opt.w)

        # b. cost per unit times quantity, summed across goods
        return par.c1*x1 + par.c2*x2 + par.c3*x3

    def welfare(self,opt=None):
        """ private utility net of the external cost """

        if opt is None: opt = self.solve(do_print=False)

        # private utility minus the cost the consumer's choice imposes on others
        return opt.u - self.externality_cost(opt)

    def revenue_utility_welfare(self,tau,goods=(2,)):
        """ revenue, utility and welfare when the same rate tau taxes each good in goods """

        # a. build the tax dict: tau on the goods in `goods`, 0 on the rest
        taus = {f'tau{j}': (tau if j in goods else 0.0) for j in (1,2,3)}
        self.set_taxes(T=0.0,**taus)

        # b. solve the consumer's problem under these taxes
        opt = self.solve(do_print=False)

        # c. revenue, utility and welfare at that solution
        R = self.tax_revenue(opt)
        u = opt.u
        W = self.welfare(opt)

        return R,u,W

    def max_welfare(self,goods=(2,),tau_max=10.0,N=1001):
        """ the welfare-maximizing tax rate -- the Pigouvian tax -- found by a grid search """

        # a. grid over the tax rate
        tau_vec = np.linspace(0,tau_max,N)

        # b. welfare at every point in the grid
        W_vec = np.empty(N)
        for i,tau in enumerate(tau_vec):
            _,_,W_vec[i] = self.revenue_utility_welfare(tau,goods=goods)

        # c. the best point
        i_best = np.argmax(W_vec)
        tau = tau_vec[i_best]
        W = W_vec[i_best]

        # d. warn if the grid ran out before the curve turned over
        if tau == tau_max:
            print(f'warning: welfare is still rising at tau_max = {tau_max:.2f} for goods {goods} -- no top found in this range')

        return tau,W
