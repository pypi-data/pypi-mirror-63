import torch
import torch.nn.functional as F
from torch import nn
from torch.nn.parameter import Parameter


class Swish(torch.autograd.Function):

    @staticmethod
    def forward(ctx, i):
        result = i * i.sigmoid()
        ctx.save_for_backward(result, i)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        result, i = ctx.saved_variables
        sigmoid_x = i.sigmoid()
        return grad_output * (result + sigmoid_x * (1 - result))


swish = Swish.apply


class Swish_module(nn.Module):
    def forward(self, x):
        return swish(x)


class TaylorActivation(nn.Module):
    def __init__(self, k):
        super(TaylorActivation, self).__init__()
        self.linear = nn.Linear(in_features=k, out_features=k)
        self.batchnorm = nn.BatchNorm1d(k)
        self.sigmoid_weights = torch.nn.init.normal_(torch.tensor(torch.zeros([k]), requires_grad=True))
        #self.sigmoid_weights = torch.tensor([0.1, 0.2, 0.3], requires_grad=True)
        self.k = k

    def forward(self, input):

        input_shape = input.shape
        input = input.view(-1)
        # pow
        pow_list = [input]
        for i in range(2, self.k+1):
            temp = input.pow(i)
            pow_list.append(temp)

        out = torch.stack(pow_list, dim=1)
        print(out.shape)
        # batchnorm
        #out = self.batchnorm(out)

        # linear
        out = self.linear(out)

        # sigmoid
        out = torch.sigmoid(self.sigmoid_weights)*out
        out = torch.sum(out, dim=1)

        out = out.view(input_shape)
        return out

class MixtureActivations_module(nn.Module):
    def __init__(self):
        super(MixtureActivations_module, self).__init__()
        self.activations = (torch.nn.Identity(), torch.nn.ReLU())
        self.weights = torch.tensor([0.5, 0.5], requires_grad=True, dtype=torch.float32)

    def forward(self, x):
        weights = torch.nn.functional.softmax(self.weights)
        out = (weights[0].item() * self.activations[0](x)) + (weights[1].item() * self.activations[1](x))
        return out

class MixtureActivationsIdReLUTanh_module(nn.Module):
    def __init__(self):
        super(MixtureActivationsIdReLUTanh_module, self).__init__()
        self.activations = (torch.nn.Identity(), torch.nn.ReLU(), torch.nn.Tanh())
        self.weights = torch.tensor([1/3, 1/3, 1/3], requires_grad=True, dtype=torch.float32)

    def forward(self, x):
        weights = torch.nn.functional.softmax(self.weights)
        out = (weights[0].item() * self.activations[0](x)) + (weights[1].item() * self.activations[1](x)) + (weights[2].item() * self.activations[2](x))
        return out


class MixtureActivationsIdReLUTanhPAU_module(nn.Module):
    def __init__(self):
        super(MixtureActivationsIdReLUTanhPAU_module, self).__init__()
        pau = Cifar_activationfunc("padeB")
        self.activations = (torch.nn.Identity(), torch.nn.ReLU(), torch.nn.Tanh(), pau.cifar_activationfunc())
        self.weights = torch.tensor([1/4, 1/4, 1/4, 1/4], requires_grad=True, dtype=torch.float32)
        1 / 0

    def forward(self, x):
        weights = torch.nn.functional.softmax(self.weights)
        out = (weights[0].item() * self.activations[0](x)) + (weights[1].item() * self.activations[1](x)) + (weights[2].item() * self.activations[2](x)) + (weights[3].item() * self.activations[3](x))
        return out

"""class PReLU_abs(nn.Module):

    def __init__(self, num_parameters=1, init=0.25):
        self.num_parameters = num_parameters
        super(PReLU_abs, self).__init__()
        self.weight = Parameter(torch.Tensor(num_parameters).fill_(init))

    @weak_script_method
    def forward(self, input):
        return F.prelu(input, torch.abs(self.weight))

    def extra_repr(self):
        return 'num_parameters={}'.format(self.num_parameters)"""


class PReLU_abs(nn.Module):

    def __init__(self, init=0.01):
        super(PReLU_abs, self).__init__()
        self.input = None
        self.weight = Parameter(torch.Tensor(1).fill_(init))

    def forward(self, input):
        self.input = input
        return self._lrelu(input)

    def _lrelu(self, x):
        x_ = x
        x_[x_ < 0] = x_[x_ < 0] * torch.abs(self.weight)
        return x_

    """
    def _lrelu_grad(self):
        grad = self.input
        grad[grad > 0] = 1.0
        grad[grad <= 0] = self.weight
        return grad

    def backward(self, gradwrtoutput):
        result = gradwrtoutput * self._lrelu_grad()
        return result"""


ACTIVATION_FUNCTIONS = dict({
    "pade_optimized_leakyrelu_abs": "pade_optimized_leakyrelu_abs",
    # "pade_optimized_leakyrelu": "pade_optimized_leakyrelu",
    "relu": nn.ReLU, "selu": nn.SELU, "leakyrelu": nn.LeakyReLU,
    "celu": nn.CELU,
    # TODO leaky relu with different alphas
    "elu": nn.ELU,
    # "tanh": F.tanh,
    "tanh": nn.Tanh,
    "relu6": nn.ReLU6,
    "swish": Swish_module,
    "softplus": nn.Softplus,
    "mixture_activations": MixtureActivations_module,
    "taylor": TaylorActivation,
    "prelu": nn.PReLU,
    "pprelu": PReLU_abs,
    "rrelu": nn.RReLU})

from pade_activation.cuda.python_imp.Pade import PADEACTIVATION_Module_based, PADEACTIVATION_Module_positive, \
    PADEACTIVATION_F_abs_cpp_versionD, PADEACTIVATION_F_cpp, \
    PADEACTIVATION_F_abs_cpp


class Cifar_activationfunc():
    def __init__(self, selected_activation_func):
        # version: a, b, c
        self.version = "a"
        if "padeA" in selected_activation_func:
            self.version = "a"
        elif "padeB" in selected_activation_func:
            self.version = "b"
        elif "padeC" in selected_activation_func:
            self.version = "c"
        elif "padeD" in selected_activation_func:
            self.version = "d"
        self.selected_activation_func = selected_activation_func

        assert "pade" in selected_activation_func or selected_activation_func in ACTIVATION_FUNCTIONS, "unknown activation function %s" % selected_activation_func

    def cifar_activationfunc(self):
        if "pade" in self.selected_activation_func:
            PADEACTIVATION_F = PADEACTIVATION_F_abs_cpp
            if "padeD" in self.selected_activation_func:
                PADEACTIVATION_F = PADEACTIVATION_F_abs_cpp_versionD
            PADEACTIVATION_F.config_cuda(5, 4, 0., self.version)

            PADEACTIVATION_Module = PADEACTIVATION_Module_based
            if "_posPau" in self.selected_activation_func:
                PADEACTIVATION_Module = PADEACTIVATION_Module_positive

            init_coefficients = self.selected_activation_func.replace("padeA", "pade").replace("padeB", "pade").replace(
                "padeC", "pade").replace("padeD", "pade").replace("_abs", "").replace("_cuda", "").replace("_posPau",
                                                                                                           "")

            return PADEACTIVATION_Module(init_coefficients=init_coefficients, act_func_cls=PADEACTIVATION_F)

        else:
            return ACTIVATION_FUNCTIONS[self.selected_activation_func]()


class Imagenet_activationfunc():
    def __init__(self, selected_activation_func):
        self.selected_activation_func = selected_activation_func
        # version: a, b, c
        self.version = "a"
        if "padeA" in selected_activation_func:
            self.version = "a"
        elif "padeB" in selected_activation_func:
            self.version = "b"
        elif "padeC" in selected_activation_func:
            self.version = "c"
        elif "padeD" in selected_activation_func:
            self.version = "d"
        self.selected_activation_func = selected_activation_func

        assert "pade" in selected_activation_func or selected_activation_func in ACTIVATION_FUNCTIONS, "unknown activation function %s" % selected_activation_func

    def imagnet_activationfunc(self):
        if "pade" in self.selected_activation_func:
            PADEACTIVATION_F_abs_cpp.config_cuda(5, 4, 0., self.version)
            init_coefficients = self.selected_activation_func.replace("_padeA", "_pade").replace("_padeB",
                                                                                                 "_pade").replace(
                "_padeC", "_pade").replace("_padeD", "_pade").replace("_abs", "").replace("_cuda", "")
            if "_abs" in self.selected_activation_func:
                return PADEACTIVATION_Module_based(init_coefficients=init_coefficients,
                                                     act_func_cls=PADEACTIVATION_F_abs_cpp)
            else:
                return PADEACTIVATION_Module_based(init_coefficients=init_coefficients,
                                                     act_func_cls=PADEACTIVATION_F_cpp)
        else:
            return ACTIVATION_FUNCTIONS[self.selected_activation_func](inplace=True)


def PAU(init_coefficients="pade_optimized_leakyrelu"):
    PADEACTIVATION_F_abs_cpp.config_cuda(5, 4, 0., "a")
    return PADEACTIVATION_Module_based(init_coefficients=init_coefficients,
                                         act_func_cls=PADEACTIVATION_F_abs_cpp)

def test_taylor():
    layer = TaylorActivation(3)
    input = torch.tensor([[1,2,3,4,5], [1,2,3,4,5]], dtype=torch.float32)
    out = layer(input)

if __name__ == '__main__':
    test_taylor()
