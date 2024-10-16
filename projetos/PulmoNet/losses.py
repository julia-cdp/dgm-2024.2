import torch


def get_disc_loss(gen, disc, criterion, input_mask, input_img, device):
    gen_img = gen(input_mask).detach()
    ans_gen = disc(gen_img)
    gt_gen = torch.zeros_like(ans_gen)
    ans_real = disc(input_img)
    gt_real = torch.ones_like(ans_real)
    # Concatenando os vetores do output do discriminador das reais com as geradas
    x = torch.cat((ans_real.reshape(-1), ans_gen.reshape(-1)))
    # Concatenando os vetores dos labels reais das images reais com as geradas
    y = torch.cat((gt_real.reshape(-1), gt_gen.reshape(-1)))
    loss = criterion(x, y)
    # The regularization (l1 norm) is not important here: is independent of D
    return loss.mean()


def get_gen_loss(gen, disc, criterion, input_mask, input_img, regularization, device, center_emphasys=None):
    gen_img = gen(input_mask)
    ans_gen = disc(gen_img)
    # we want ans_gen close to 1: to trick the disc
    gt_gen = torch.ones_like(ans_gen)
    loss_pt1 = criterion(ans_gen, gt_gen).mean()
    if center_emphasys is True:
        loss_pt2 = torch.sum(torch.abs(input_mask*(input_img-gen_img)), dim=(1, 2)).mean()
        loss_pt3 = torch.sum(torch.abs((1-input_mask)*(input_img-gen_img)), dim=(1, 2)).mean()
        return loss_pt1+(2*regularization/3)*loss_pt2+(regularization/3)*loss_pt3
    else:
        loss_pt2 = torch.sum(torch.abs(input_img-gen_img), dim=(1, 2)).mean()
        return loss_pt1+regularization*loss_pt2
