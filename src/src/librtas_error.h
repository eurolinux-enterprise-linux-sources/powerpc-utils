/**
 * @file librtas_error.h
 * @brief Common librtas_error routine for powerpc-utils-papr commands
 *
 * Copyright (c) 2004 International Business Machines
 * Common Public License Version 1.0 (see COPYRIGHT)
 *
 * @author Nathan Fontenot <nfont@linux.vnet.ibm.com>
 */

#ifndef _LIBRTAS_ERROR_H
#define _LIBRTAS_ERROR_H

void librtas_error(int, char *, size_t);
int is_librtas_error(int);

#endif
