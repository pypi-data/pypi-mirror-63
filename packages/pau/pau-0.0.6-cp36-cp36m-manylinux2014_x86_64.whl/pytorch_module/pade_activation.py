from time import time

import torch
from pade_activation.pade_activation_v1 import *

class PADEACTIVATION_V5(PADEACTIVATION):

    def __init__(self, debug=False, n_features=10, selected_constants_for_inits="pade_softplus_center", inplace=False):
        super(PADEACTIVATION_V5, self).__init__(debug=debug, n_features=n_features,
                                                selected_constants_for_inits=selected_constants_for_inits,
                                                inplace=inplace)

        self.activation_function = PADEACTIVATION_F.apply

    def forward(self, x):
        out = self.activation_function(x, self.weight_numerator, self.weight_denominator)
        # out = self.activation_function((x, self.weight_numerator, self.weight_denominator))

        return out


class PADEACTIVATION_V5_memory(PADEACTIVATION):

    def __init__(self, debug=False, n_features=10, selected_constants_for_inits="pade_softplus_center", inplace=False):
        super(PADEACTIVATION_V5_memory, self).__init__(debug=debug, n_features=n_features,
                                                       selected_constants_for_inits=selected_constants_for_inits,
                                                       inplace=inplace)

        self.activation_function = PADEACTIVATION_F_memory.apply

    def forward(self, x):
        out = self.activation_function(x, self.weight_numerator, self.weight_denominator)

        """
        print(id(self),
              torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              self.weight_numerator.detach().cpu().numpy().tolist(),
              self.weight_denominator.detach().cpu().numpy().tolist())
        """
        """print(id(self),
              # torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              # torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              self.weight_numerator.detach().cpu().numpy().tolist(),
              self.weight_denominator.detach().cpu().numpy().tolist())"""
        return out


class PADEACTIVATION_V5_memory_grad_norm(PADEACTIVATION):

    def __init__(self, debug=False, n_features=10, selected_constants_for_inits="pade_softplus_center", inplace=False):
        super(PADEACTIVATION_V5_memory_grad_norm, self).__init__(debug=debug, n_features=n_features,
                                                selected_constants_for_inits=selected_constants_for_inits,
                                                                 inplace=inplace)

        self.activation_function = PADEACTIVATION_F_memory_grad_norm.apply

    def forward(self, x):
        out = self.activation_function(x, self.weight_numerator, self.weight_denominator)

        """
        print(id(self),
              torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              torch.max(torch.abs(x)).detach().cpu().numpy().tolist(),
              self.weight_numerator.detach().cpu().numpy().tolist(),
              self.weight_denominator.detach().cpu().numpy().tolist())
        """
        return out


class PADEACTIVATION_F(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, weight_numerator, weight_denominator):
        ctx.save_for_backward(weight_numerator, weight_denominator)

        z = input

        clamped_n = weight_numerator.clamp(min=0)
        clamped_d = weight_denominator.clamp(min=0)

        numerator = z.mul(clamped_n[1]) + clamped_n[0]
        xps = list()

        xps.append(z)
        for c_n in clamped_n[2:]:
            xp = xps[-1].mul(z)
            xps.append(xp)
            numerator = numerator + c_n.mul(xp)

        denominator = z * clamped_d[0] + 1
        for idx, c_d in enumerate(clamped_d[1:]):
            xp = xps[idx + 1]
            denominator = denominator + c_d.mul(xp)

        ctx.xps = torch.stack(xps)
        ctx.denominator = denominator
        ctx.numerator = numerator
        return numerator.div(denominator)

    @staticmethod
    def backward(ctx, grad_output):

        weight_numerator, weight_denominator = ctx.saved_tensors
        weight_numerator = weight_numerator.clamp(min=0)
        weight_denominator = weight_denominator.clamp(min=0)

        P = ctx.numerator
        Q = ctx.denominator
        xps = ctx.xps

        dfdn = torch.cat(((1.0 / Q).unsqueeze(dim=0), xps.div(Q)))

        dfdd_tmp = (-P.div((Q.mul(Q))))
        dfdd = dfdd_tmp.mul(xps[0:weight_denominator.size()[0]])

        dfdx1 = 2.0 * weight_numerator[2].mul(xps[0]) + weight_numerator[1]
        for idx, xp in enumerate(xps[1:weight_numerator.size()[0]-2]):
            i = (idx + 3)
            dfdx1 += i * weight_numerator[i].mul(xp)
        dfdx1 = dfdx1.div(Q)

        dfdx2 = 2.0 * weight_denominator[1].mul(xps[0]) + weight_denominator[0]
        for idx, xp in enumerate(xps[1:weight_denominator.size()[0]-1]):
            i = (idx + 3)
            dfdx2 += i * weight_denominator[idx+2].mul(xp)
        dfdx2_ = dfdx2
        dfdx2 = dfdx2_.mul(dfdd_tmp)

        dfdx = dfdx1 + dfdx2

        rdfdn = torch.mul(grad_output, dfdn)
        rdfdd = torch.mul(grad_output, dfdd)

        dfdn = rdfdn
        dfdd = rdfdd
        for _ in range(len(P.shape)):
            dfdn = dfdn.sum(-1)
            dfdd = dfdd.sum(-1)
        dfdx = grad_output.mul(dfdx)
        #print(dfdx)
        #print(dfdx)
        #print(dfdn)
        #print(dfdd)
        return dfdx, dfdn, dfdd
        #return dfdx.clamp(-1,1), dfdn.clamp(-1,1), dfdd.clamp(-1,1)


class PADEACTIVATION_F_memory(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, weight_numerator, weight_denominator):
        ctx.save_for_backward(input, weight_numerator, weight_denominator)

        z = input

        clamped_n = weight_numerator#.clamp(min=0, max=1.)
        clamped_d = weight_denominator.clamp(min=0)
        #print(weight_denominator)
        #print(torch.min(z), torch.max(z))

        numerator = z.mul(clamped_n[1]) + clamped_n[0]
        xps = list()
        #xp = z
        xps.append(z)
        for c_n in clamped_n[2:]:
            xp = xps[-1].mul(z)
            xps.append(xp)
            numerator = numerator + c_n.mul(xp)

        denominator = z * clamped_d[0] + 1
        for idx, c_d in enumerate(clamped_d[1:]):
            xp = xps[idx + 1]
            denominator = denominator + c_d.mul(xp)

        return numerator.div(denominator)

    @staticmethod
    def backward(ctx, grad_output):
        #print(grad_output)
        #1 / 0
        x, weight_numerator, weight_denominator = ctx.saved_tensors
        #print(weight_numerator.detach().cpu().numpy().tolist(), weight_denominator.detach().cpu().numpy().tolist())

        #grad_input = grad_output.clone()

        clamped_n = weight_numerator#.clamp(min=0, max=1.)
        clamped_d = weight_denominator.clamp(min=0)
        numerator = x.mul(clamped_n[1]) + clamped_n[0]
        xps = list()
        # xp = z
        xps.append(x)
        for c_n in clamped_n[2:]:
            xp = xps[-1].mul(x)
            xps.append(xp)
            numerator = numerator + c_n.mul(xp)

        denominator = x * clamped_d[0] + 1
        for idx, c_d in enumerate(clamped_d[1:]):
            xp = xps[idx + 1]
            denominator = denominator + c_d.mul(xp)

        xps = torch.stack(xps)
        P = numerator
        Q = denominator

        dfdn = torch.cat(((1.0 / Q).unsqueeze(dim=0), xps.div(Q)))

        dfdd_tmp = (-P.div((Q.mul(Q))))
        dfdd = dfdd_tmp.mul(xps[0:clamped_d.size()[0]])

        dfdx1 = 2.0 * clamped_n[2].mul(xps[0]) + clamped_n[1]
        for idx, xp in enumerate(xps[1:clamped_n.size()[0]-2]):
            i = (idx + 3)
            dfdx1 += i * clamped_n[i].mul(xp)
        dfdx1 = dfdx1.div(Q)

        dfdx2 = 2.0 * clamped_d[1].mul(xps[0]) + clamped_d[0]
        for idx, xp in enumerate(xps[1:clamped_d.size()[0]-1]):
            i = (idx + 3)
            dfdx2 += i * clamped_d[idx+2].mul(xp)
        dfdx2_ = dfdx2
        dfdx2 = dfdx2_.mul(dfdd_tmp)

        dfdx = dfdx1 + dfdx2

        rdfdn = torch.mul(grad_output, dfdn)
        rdfdd = torch.mul(grad_output, dfdd)

        dfdn = rdfdn
        dfdd = rdfdd
        for _ in range(len(P.shape)):
            dfdn = dfdn.sum(-1)
            dfdd = dfdd.sum(-1)
        dfdx = grad_output.mul(dfdx)
        #print(dfdx)
        #print(dfdn)
        #print(dfdd)
        return dfdx, dfdn, dfdd
        #return dfdx.clamp(-0.5, 0.5), dfdn, dfdd
        #return dfdx.clamp(-3,3), dfdn.clamp(-3,3), dfdd.clamp(-3,3)


class PADEACTIVATION_F_memory_grad_norm(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, weight_numerator, weight_denominator):
        ctx.save_for_backward(input, weight_numerator, weight_denominator)

        z = input

        clamped_n = weight_numerator#.clamp(min=0, max=1.)
        clamped_d = weight_denominator.clamp(min=0)
        #print(weight_denominator)
        #print(torch.min(z), torch.max(z))

        numerator = z.mul(clamped_n[1]) + clamped_n[0]
        xps = list()
        #xp = z
        xps.append(z)
        for c_n in clamped_n[2:]:
            xp = xps[-1].mul(z)
            xps.append(xp)
            numerator = numerator + c_n.mul(xp)

        denominator = z * clamped_d[0] + 1
        for idx, c_d in enumerate(clamped_d[1:]):
            xp = xps[idx + 1]
            denominator = denominator + c_d.mul(xp)

        return numerator.div(denominator)

    @staticmethod
    def backward(ctx, grad_output):
        #print(grad_output)
        #1 / 0
        x, weight_numerator, weight_denominator = ctx.saved_tensors
        #print(weight_numerator.detach().cpu().numpy().tolist(), weight_denominator.detach().cpu().numpy().tolist())

        #grad_input = grad_output.clone()

        clamped_n = weight_numerator#.clamp(min=0, max=1.)
        clamped_d = weight_denominator.clamp(min=0)
        numerator = x.mul(clamped_n[1]) + clamped_n[0]
        xps = list()
        # xp = z
        xps.append(x)
        for c_n in clamped_n[2:]:
            xp = xps[-1].mul(x)
            xps.append(xp)
            numerator = numerator + c_n.mul(xp)

        denominator = x * clamped_d[0] + 1
        for idx, c_d in enumerate(clamped_d[1:]):
            xp = xps[idx + 1]
            denominator = denominator + c_d.mul(xp)

        xps = torch.stack(xps)
        P = numerator
        Q = denominator

        dfdn = torch.cat(((1.0 / Q).unsqueeze(dim=0), xps.div(Q)))

        dfdd_tmp = (-P.div((Q.mul(Q))))

        #####
        # gradient regularization
        dfdd_tmp2 = dfdd_tmp.clone().detach()
        idx_tmp = Q <= 1
        q_normed = 2*Q[idx_tmp] - torch.exp(torch.tensor(10.))
        dfdd_tmp2[idx_tmp] += q_normed
        #####
        dfdd = dfdd_tmp2.mul(xps[0:clamped_d.size()[0]])
        # regularization wrong with magic
        #for idx in range(dfdd.shape[0]):
        #    dfdd[idx][Q <= 1] = dfdd[idx].mul(1 + (2 * (Q - torch.exp(torch.tensor(10.)))))[Q <= 1]

        dfdx1 = 2.0 * clamped_n[2].mul(xps[0]) + clamped_n[1]
        for idx, xp in enumerate(xps[1:clamped_n.size()[0]-2]):
            i = (idx + 3)
            dfdx1 += i * clamped_n[i].mul(xp)
        dfdx1 = dfdx1.div(Q)

        dfdx2 = 2.0 * clamped_d[1].mul(xps[0]) + clamped_d[0]
        for idx, xp in enumerate(xps[1:clamped_d.size()[0]-1]):
            i = (idx + 3)
            dfdx2 += i * clamped_d[idx+2].mul(xp)
        dfdx2_ = dfdx2
        dfdx2_normed = dfdx2[idx_tmp] * (q_normed - torch.exp(torch.tensor(10.)))
        dfdx2 = dfdx2_.mul(dfdd_tmp)

        dfdx = dfdx1 + dfdx2

        #####
        # gradient regularization
        dfdx[idx_tmp] += dfdx2_normed
        #####

        rdfdn = torch.mul(grad_output, dfdn)
        rdfdd = torch.mul(grad_output, dfdd)

        dfdn = rdfdn
        dfdd = rdfdd
        for _ in range(len(P.shape)):
            dfdn = dfdn.sum(-1)
            dfdd = dfdd.sum(-1)
        dfdx = grad_output.mul(dfdx)
        #print(dfdx)
        #print(dfdn)
        #print(dfdd)
        return dfdx, dfdn, dfdd
        #return dfdx.clamp(-0.5, 0.5), dfdn, dfdd
        #return dfdx.clamp(-3,3), dfdn.clamp(-3,3), dfdd.clamp(-3,3)


if __name__ == '__main__':
    v5 = PADEACTIVATION_V5()
    v5_memory = PADEACTIVATION_V5_memory()