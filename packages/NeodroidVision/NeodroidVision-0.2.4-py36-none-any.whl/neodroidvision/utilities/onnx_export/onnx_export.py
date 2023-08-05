import numpy
import torch


def export(model, model_export_name, latest, batch_size=1):
    model.train(False)
    # Input to the model
    x = torch.randn(batch_size, 3, 224, 224, requires_grad=True, dtype=torch.float32)

    # Export the model
    torch_out = torch.onnx._export(
        model.to("cpu"),  # model being run
        x,  # model input (or a tuple for multiple inputs)
        model_export_name,
        export_params=True,  # store the trained parameter weights inside
        verbose=True,
    )
    import onnx
    import caffe2.python.onnx.backend as onnx_caffe2_backend

    # Load the ONNX ModelProto object. model is a standard Python protobuf object
    model = onnx.load(model_export_name)

    # prepare the caffe2 backend for executing the model this converts the ONNX model into a
    # Caffe2 NetDef that can execute it. Other ONNX backends, like one for CNTK will be
    # availiable soon.
    prepared_backend = onnx_caffe2_backend.prepare(model)

    # run the model in Caffe2

    # Construct a map from input names to Tensor data.
    # The graph of the model itself contains inputs for all weight parameters, after the input image.
    # Since the weights are already embedded, we just need to pass the input image.
    # Set the first input.
    W = {model.graph.input[0].name: x.data.numpy()}

    # Run the Caffe2 net:
    c2_out = prepared_backend.run(W)[0]

    # Verify the numerical correctness upto 3 decimal places
    numpy.testing.assert_almost_equal(torch_out.data.cpu().numpy(), c2_out, decimal=3)

    print(
        "Exported model has been executed on Caffe2 backend, and the result looks good!"
    )

    # extract the workspace and the model proto from the internal representation
    c2_workspace = prepared_backend.workspace
    c2_model = prepared_backend.predict_net

    # Now import the caffe2 mobile exporter
    from caffe2.python.predictor import mobile_exporter

    print("Exporting to mobile")

    # call the Export to get the predict_net, init_net. These nets are needed for running things on mobile
    init_net, predict_net = mobile_exporter.Export(
        c2_workspace, c2_model, c2_model.external_input
    )

    # Let's also save the init_net and predict_net to a file that we will later use for running them on mobile
    with open(str(latest + "/init_net.pb"), "wb") as f:
        f.write(init_net.SerializeToString())

    with open(str(latest + "/predict_net.pb"), "wb") as f:
        f.write(c2_model.SerializeToString())
