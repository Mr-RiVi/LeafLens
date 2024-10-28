import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    OutlinedInput,
    InputLabel,
    IconButton,
} from "@mui/material";

import CloseIcon from '@mui/icons-material/Close';

import { DataStruct } from "../../types/types.ts";
import { Field, Form, Formik } from "formik";

/**
 * A reusable functional component that represents a Material-UI dialog/modal.
 * @param {Object} props - The props passed to the component.
 * @param {boolean} props.open - Controls the visibility of the dialog.
 * @param {Function} props.onClose - Callback function to handle the closing of the dialog.
 * @returns {JSX.Element} - The rendered component.
 */

type DialogProps = {
    open: boolean;
    onClose: (value: boolean) => void;
    content: DataStruct;
};

const ProductCreationDialog = (props: DialogProps) => {
    const initialFormValues = {
        projectDisplayName: '',
        projectDescription: ''
    };

    const submitHandler = (values: typeof initialFormValues) => {
        console.log(values);
        // TODO: reset form
    }

    const handleClose = (event: React.SyntheticEvent, reason: "backdropClick" | "escapeKeyDown") => {
        if (reason === "backdropClick") return; // Prevent closing on backdrop click
        props.onClose(false); // Allow closing for other reasons, such as escape key or close button
    };
    return (
        <>
            <Dialog
                fullWidth={true}
                maxWidth={"sm"}
                open={props.open}
                onClose={handleClose}
            >
                <DialogTitle
                    sx={{ textAlign: 'center', fontWeight: 'bold' }}
                >
                    Create New Project
                </DialogTitle>
                <IconButton
                    aria-label="close"
                    onClick={() => props.onClose(false)}
                    sx={(theme) => ({
                        position: 'absolute',
                        right: 8,
                        top: 8,
                        color: theme.palette.grey[500],
                    })}
                >
                    <CloseIcon />
                </IconButton>
                <Formik
                    initialValues={initialFormValues}
                    onSubmit={submitHandler}
                >
                    {({ values }) => (
                        <Form>
                            <DialogContent
                                sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: 2,
                                    alignItems: 'stretch',
                                    mt: 2,
                                }}
                            >
                                <InputLabel>Project Display Name</InputLabel>
                                <Field
                                    name="projectDisplayName"
                                    as={OutlinedInput}
                                    id="projectDisplayName"
                                    placeholder="Project Display Name"
                                    fullWidth
                                    sx={{ mb: 2 }}
                                />
                                <InputLabel>Project Description (Optional)</InputLabel>
                                <Field
                                    name="projectDescription"
                                    as={OutlinedInput}
                                    id="projectDescription"
                                    placeholder="Project Description"
                                    fullWidth
                                    sx={{ mb: 2 }}
                                    multiline rows={3}
                                />
                            </DialogContent>
                            <DialogActions>
                                <Button
                                    onClick={() => props.onClose(false)}
                                    variant="outlined"
                                >
                                    Back
                                </Button>
                                <Button
                                    type="submit"
                                    variant="contained"
                                    color="primary"
                                    disabled={!values.projectDisplayName}
                                >
                                    Create
                                </Button>
                            </DialogActions>
                        </Form>
                    )}
                </Formik>
            </Dialog>
        </>
    );
};

export default ProductCreationDialog;
