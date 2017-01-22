import os
import sys
import time
import shlex
import subprocess


main_prog = "python neural_painter.py"
img_size = "--image_size 800x800"

inp_non_lin_switch = "--nonlin "
out_non_lin_switch = "--output_nonlin "

neurons_switch = "--hidden_size "
hidden_layer_switch = "--nr_hidden "

output_layers_switch = "--nr_channel 3"

seed_switch = "--seed "

output_switch = "--output "

coord_bias_switch = "--coord_bias"
recurrent_switch = "--recurrent"
batch_norm_switch1 = "--batch_norm --batch_norm_position before_nonlin"
batch_norm_switch2 = "--batch_norm --batch_norm_position after_nonlin"
extra_switches = dict(
    no_extra="",
    bias=coord_bias_switch,
    rec=recurrent_switch,
    # batch1=batch_norm_switch1,
    # batch2=batch_norm_switch2,
    bias_rec=" ".join([coord_bias_switch, recurrent_switch]),
    # bias_batch_norm1=" ".join([coord_bias_switch, batch_norm_switch1]),
    # bias_batch_norm2=" ".join([coord_bias_switch, batch_norm_switch2]),
    # rec_batch_norm1=" ".join([recurrent_switch, batch_norm_switch1]),
    # rec_batch_norm2=" ".join([recurrent_switch, batch_norm_switch2]),
    bias_rec_bnorm1=" ".join(
        [coord_bias_switch, recurrent_switch, batch_norm_switch1]),
    bias_rec_bnorm2=" ".join(
        [coord_bias_switch, recurrent_switch, batch_norm_switch2]),
)


non_linear_func = [
    "abs", "relu", "tanh", "abs_tanh", "sigmoid", "softplus", "sin", "cos",
    "sgn", "sort", "log_abs", "log_abs_p1", "log_relu", "log_square",
    "xlogx_abs", "xlogx_abs_p1", "xlogx_relu", "xlogx_relu_p1",
    "xlogx_square", "softmax", "logsoftmax", "hard_sigmoid", "identity",
    "square", "random_every_time", "random_once"
]

total = len(non_linear_func) * len(non_linear_func) * \
    len(extra_switches) * 2 * 3

count = 0

for func1 in non_linear_func:
    input_func = inp_non_lin_switch + func1
    func_dir1 = os.path.join("outputs", func1)
    os.mkdir(func_dir1)
    # print(func_dir1)

    for func2 in non_linear_func:
        output_func = out_non_lin_switch + func2
        func_dir2 = os.path.join(func_dir1, func2)
        os.mkdir(func_dir2)
        # print(func_dir2)

        for extra_switch in extra_switches:
            extra_dir = os.path.join(func_dir2, extra_switch)
            os.mkdir(extra_dir)
            # print(extra_dir)

            for layers in [1, 3]:
                hidden_layers = hidden_layer_switch + str(layers)

                for neurons in [1, 10, 100]:
                    neurons_per_layer = neurons_switch + str(neurons)

                    for seed in [131]:
                        seed_opt = seed_switch + str(seed)

                        file_name = "{}-{}-{}.png".format(layers,
                                                          neurons, seed)
                        file_path = os.path.join(extra_dir, file_name)
                        # print(file_path)
                        output_file_switch = output_switch + file_path

                        command = "{} {} {} {} {} {} {} {} {} {}".format(
                            main_prog,
                            img_size,
                            input_func,
                            output_func,
                            hidden_layers,
                            neurons_per_layer,
                            seed_opt,
                            output_layers_switch,
                            extra_switches[extra_switch],
                            output_file_switch
                        )

                        # print(command)
                        final_command = shlex.split(command)

                        count += 1
                        print("====")
                        print(count, "/", total, "(", count * 100 / total, "% )")
                        time1 = time.time()

                        p = subprocess.Popen(
                            final_command, universal_newlines=True, bufsize=1, stdout=subprocess.PIPE)

                        for line in iter(p.stdout.readline, ""):
                            print(line, end="")
                            sys.stdout.flush()

                        # output = p.communicate()[0]
                        # print(output)
                        # subprocess.call(final_command)
                        # subprocess.run(final_command)
                        # print(subprocess.check_output(final_command))

                        print(time.time() - time1)

                    # sys.exit()

                # print(final_command)
                # print("=======")
