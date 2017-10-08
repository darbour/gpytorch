from .. import libfft


def fft1(input):
    # [..., d]
    orig_size = input.size()
    orig_type = type(input)

    input = input.view(-1, input.size(-1))
    n, d = input.size()

    output = input.new().cpu().resize_(n, (d // 2) + 1, 2)
    libfft.fft1_r2c(input.cpu().float(), output)

    if input.is_cuda:
        output = output.cuda()    

    if len(orig_size) > 1:
        output_size = list(orig_size[:-1]) + [(d // 2) + 1, 2]
    else:
        output_size = [(d // 2) + 1, 2]
    return output.view(*output_size).type(orig_type)


def ifft1(input, size=None):
    # [..., d, 2]
    orig_type = type(input)

    if not size:
        size = list(input.size())[:-1]
        d = (size[-1] - 1) * 2
        size[-1] = d
    else:
        d = size[-1]
    input = input.view(-1, *input.size()[-2:])

    output = input.new().cpu().resize_(input.size(0), d)
    libfft.fft1_c2r(input.cpu(), output)
    if input.is_cuda:
        output = output.cuda()
    output.div_(d)
    return output.view(size).type(orig_type)
